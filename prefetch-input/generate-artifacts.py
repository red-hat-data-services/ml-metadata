#!/usr/bin/env python3
"""Convert Bazel resolved repositories and downloaded Bazel tools to Hermeto JSON/YAML.

Run after fresh online dependency analysis for each Linux architecture. JSON is a
YAML subset, so the output is a valid artifacts.lock.yaml without PyYAML.
"""

import argparse
import ast
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re


TOOL_URLS = {
    "x86_64": "https://github.com/bazelbuild/bazel/releases/download/6.3.2/bazel-6.3.2-linux-x86_64",
    "aarch64": "https://github.com/bazelbuild/bazel/releases/download/6.3.2/bazel-6.3.2-linux-arm64",
    "ppc64le": "https://ftp2.osuosl.org/pub/ppc64el/bazel/el8/bazel-6.3.2",
}


def varint(stream):
    value = 0
    for shift in range(0, 70, 7):
        byte = stream.read(1)
        if not byte:
            raise ValueError("Truncated Bazel workspace log")
        value |= (byte[0] & 127) << shift
        if byte[0] < 128:
            return value
    raise ValueError("Invalid protobuf varint")


def read_exact(stream, size):
    data = stream.read(size)
    if len(data) != size:
        raise ValueError("Truncated Bazel workspace log")
    return data


def protobuf_fields(data):
    stream = BytesIO(data)
    fields = {}
    while stream.tell() < len(data):
        tag = varint(stream)
        field, wire = tag >> 3, tag & 7
        if wire == 0:
            value = varint(stream)
        elif wire == 2:
            value = read_exact(stream, varint(stream))
        elif wire in (1, 5):
            value = read_exact(stream, 8 if wire == 1 else 4)
        else:
            raise ValueError(f"Unsupported protobuf wire type {wire}")
        fields.setdefault(field, []).append(value)
    return fields


def workspace_artifacts(paths):
    # Bazel 6.3.2 WorkspaceEvent: context=2, download=4, download_and_extract=5.
    # Both download messages have url=1 and sha256=3. See the upstream schema:
    # src/main/java/com/google/devtools/build/lib/bazel/debug/workspace_log.proto
    artifacts = []
    for path in paths:
        initial_count = len(artifacts)
        data = path.read_bytes()
        stream = BytesIO(data)
        while stream.tell() < len(data):
            event = protobuf_fields(read_exact(stream, varint(stream)))
            for kind in (4, 5):
                if kind not in event:
                    continue
                download = protobuf_fields(event[kind][0])
                digest = download.get(3, [b""])[0].decode()
                context = event.get(2, [b"unknown"])[0].decode()
                if not re.fullmatch(r"[0-9a-f]{64}", digest):
                    raise ValueError(f"{path}: {context}: download without a SHA-256 pin")
                urls = [url.decode() for url in download.get(1, [])]
                url = next((url for url in urls if url.startswith("https://")), None)
                if not url:
                    raise ValueError(f"{path}: {context}: download without an HTTPS URL")
                artifacts.append({"download_url": url, "checksum": f"sha256:{digest}",
                                  "filename": digest})
        if len(artifacts) == initial_count:
            raise ValueError(f"{path}: no downloads recorded; use a fresh Bazel output base")
    return artifacts


def read_resolved(path):
    # Never execute a .bzl file as Python.
    tree = ast.parse(path.read_text(), filename=str(path))
    for statement in tree.body:
        if isinstance(statement, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "resolved"
            for target in statement.targets
        ):
            return ast.literal_eval(statement.value)
    raise ValueError(f"{path}: no literal resolved assignment")


def repository_artifacts(paths):
    artifacts = {}
    for path in paths:
        for entry in read_resolved(path):
            for repo in entry.get("repositories", []):
                attrs = repo.get("attributes", {})
                if repo.get("rule_class", "").endswith("%_go_download_sdk"):
                    # Include the SDK for every cluster architecture, even when
                    # discovery was performed on only one host architecture.
                    if not attrs.get("sdks"):
                        raise ValueError(f"{path}: pin the Go SDK metadata before generating the lockfile")
                    for platform in ("linux_amd64", "linux_arm64", "linux_ppc64le"):
                        filename, digest = attrs["sdks"][platform]
                        if not re.fullmatch(r"[0-9a-f]{64}", digest):
                            raise ValueError(f"Invalid Go SDK checksum: {platform}")
                        artifacts[digest] = {
                            "download_url": f"https://dl.google.com/go/{filename}",
                            "checksum": f"sha256:{digest}", "filename": digest,
                        }
                    continue
                urls = attrs.get("urls") or [attrs.get("url")]
                urls = [url for url in urls if url]
                if not urls:
                    # Local configuration rules do not download anything. Custom
                    # rules may: the fresh offline build remains the coverage check.
                    continue
                digest = attrs.get("sha256", "")
                if not re.fullmatch(r"[0-9a-f]{64}", digest):
                    raise ValueError(
                        f"{path}: {attrs.get('name')}: pin sha256 in the repository rule "
                        "and regenerate; Bazel cannot reliably use its offline cache without it"
                    )
                url = next((url for url in urls if url.startswith("https://")), None)
                if not url:
                    raise ValueError(f"{path}: no HTTPS URL for {attrs.get('name')}")
                artifacts.setdefault(digest, {
                    "download_url": url,
                    "checksum": f"sha256:{digest}",
                    "filename": digest,
                })
    if not artifacts:
        raise ValueError("No downloadable repositories found; use fresh Bazel output bases")
    return [artifacts[key] for key in sorted(artifacts)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resolved", type=Path, nargs="+", required=True)
    parser.add_argument("--workspace-log", type=Path, nargs="+", required=True,
                        help="Bazel --experimental_workspace_rules_log_file outputs")
    parser.add_argument("--tools-dir", type=Path, required=True,
                        help="Contains bazel-6.3.2-linux-{x86_64,aarch64,ppc64le}")
    parser.add_argument("--output", type=Path, default=Path("prefetch-input/artifacts.lock.yaml"))
    args = parser.parse_args()
    by_checksum = {artifact["checksum"]: artifact
                   for artifact in repository_artifacts(args.resolved)}
    for artifact in workspace_artifacts(args.workspace_log):
        by_checksum.setdefault(artifact["checksum"], artifact)
    artifacts = [by_checksum[key] for key in sorted(by_checksum)]
    for arch, url in TOOL_URLS.items():
        filename = f"bazel-6.3.2-linux-{arch}"
        digest = hashlib.sha256()
        with (args.tools_dir / filename).open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        artifacts.append({"download_url": url, "checksum": f"sha256:{digest.hexdigest()}",
                          "filename": filename})
    # Only write once every input has passed validation.
    args.output.write_text(json.dumps({"metadata": {"version": "1.0"},
                                       "artifacts": artifacts}, indent=2) + "\n")


if __name__ == "__main__":
    main()
