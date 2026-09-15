# Hermetic MLMD dependency lockfiles

`rpms.lock.yaml` and `artifacts.lock.yaml` contain resolved download URLs and
checksums. Both local PipelineRuns now enable hermetic mode, prefetch RPM and
generic dependencies from this directory, and use `Dockerfile.konflux.hermetic`.
Full compilation and runtime testing remain for the cluster.

Validation: Hermeto fetched and verified all 58 generic artifacts. A fresh
aarch64 Bazel analysis passed with `--network none` and
`--experimental_repository_disable_download`, using only the prefetched cache.
The RPM lockfile contains 259 binary packages for aarch64, 260 for ppc64le, and
259 for x86_64, plus available source RPMs.

The RPM lockfile was generated with rpm-lockfile-prototype 0.30.1 for x86_64,
aarch64, and ppc64le using public UBI 9 repositories. The bare context includes
the complete package closure for both container stages, including runtime
`tzdata`. The resolver could not find source RPMs for the current `kernel-headers`
package in public UBI; its binary packages are locked for all three architectures.

The generic lockfile is generated from Bazel 6.3.2 repository definitions **and
actual repository download logs**. Logs include downloads hidden inside custom
rules, such as Flex, Bison, and M4. All three Linux Bazel executables and Go SDKs
are included. The Go SDK version remains 1.18, as selected by gRPC; a patch pins
its per-platform metadata so it no longer downloads an unpinned `versions.json`.
MariaDB uses the same 3.0.8 release through a checksummed source archive.

Dependency discovery does not compile MLMD. Native aarch64 analysis and analysis
of the x86_64/ppc64le platform configurations on the aarch64 host are used to
collect downloads. The latter uses a temporary compiler registration strictly
for analysis; it does not verify those architectures' native compilers or build
results. Native cluster builds are the final coverage check.

## Refresh RPM dependencies

On Linux with [rpm-lockfile-prototype](https://github.com/konflux-ci/rpm-lockfile-prototype)
installed, run from this directory:

```bash
rpm-lockfile-prototype --outfile rpms.lock.yaml rpms.in.yaml
```

If a package is unavailable in public UBI, configure the appropriate RHEL
repositories and subscription access before resolving again.

## Refresh Bazel dependencies

Prefer native Linux builders for x86_64, aarch64, and ppc64le. Run from the
repository root on each builder:

```bash
arch=$(uname -m)
mkdir -p prefetch-input/generated/tools
podman build --no-cache -f prefetch-input/Dockerfile.resolve -t localhost/mlmd-resolve .
container=$(podman create localhost/mlmd-resolve)
podman cp "$container:/tmp/resolved.bzl" "prefetch-input/generated/resolved-$arch.bzl"
podman cp "$container:/tmp/workspace.log" "prefetch-input/generated/workspace-$arch.log"
podman cp "$container:/usr/local/bin/bazel" "prefetch-input/generated/tools/bazel-6.3.2-linux-$arch"
podman rm "$container"
```

Always use fresh Bazel output bases: cached repositories can be omitted from the
resolved file and download log. `Dockerfile.resolve` runs `bazel build --nobuild`
with the same target and build options as the hermetic builder.

Collect the files from all three builders in `prefetch-input/generated/`, then:

```bash
python3 prefetch-input/generate-artifacts.py \
  --resolved prefetch-input/generated/resolved-{x86_64,aarch64,ppc64le}.bzl \
  --workspace-log prefetch-input/generated/workspace-{x86_64,aarch64,ppc64le}.log \
  --tools-dir prefetch-input/generated/tools
```

The generator rejects unpinned downloads, deduplicates archives by checksum, and
hashes the downloaded Bazel executables. Review executable hashes against the
distributors' checksums where available. Refresh after changes to Bazel,
repository definitions, patches, or toolchains. Custom rules that execute git,
curl, or other download tools may require additional offline handling; the
network-disabled cluster build detects these.

## Cluster testing

Commit the lockfiles, application changes, and local `.tekton` changes together,
then trigger the PR build as usual. Check `prefetch-dependencies` and all three
architecture builds. The hermetic Dockerfile consumes the injected local RPM
repositories and generic downloads at `/cachi2/output`, and explicitly disables
Bazel's repository downloader. It retains the existing pinned base images.

For a local prefetch check with [Hermeto](https://hermetoproject.github.io/hermeto/):

```bash
hermeto fetch-deps --source . --output prefetch-input/generated/hermeto-output \
  "$(cat prefetch-input/prefetch.json)"
```

Keep generated caches and logs out of Git. Update konflux-central after cluster
testing, as planned.
