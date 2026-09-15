#!/usr/bin/env bash
set -euo pipefail

generic_dir=${1:-/cachi2/output/deps/generic}
cache_dir=${2:-/opt/bazel-repository-cache}
arch=$(uname -m)
case "$arch" in
  x86_64|aarch64|ppc64le) ;;
  *) echo "Unsupported architecture: $arch" >&2; exit 1 ;;
esac
install -m 0755 "$generic_dir/bazel-6.3.2-linux-$arch" /usr/local/bin/bazel

count=0
for artifact in "$generic_dir"/*; do
  digest=${artifact##*/}
  [[ "$digest" =~ ^[0-9a-f]{64}$ ]] || continue
  printf '%s  %s\n' "$digest" "$artifact" | sha256sum --check --status
  mkdir -p "$cache_dir/content_addressable/sha256/$digest"
  cp "$artifact" "$cache_dir/content_addressable/sha256/$digest/file"
  count=$((count + 1))
done
if [[ "$count" -eq 0 ]]; then
  echo 'No Bazel repository artifacts were prefetched' >&2
  exit 1
fi
