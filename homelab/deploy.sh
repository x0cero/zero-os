#!/bin/sh
# From the Mac: fetch the newest qcow2 built by GitHub and boot it as VM 303
# on the homelab. Pass a run id to pick a specific "Build disk images" run.
set -eu
PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
HOST=${ZERO_OS_HOST:-homelab}
export GH_TOKEN=$(gh auth token -u x0cero)
RUN=${1:-$(gh run list -R x0cero/zero-os --workflow "Build disk images" --status success --limit 1 --json databaseId -q '.[0].databaseId')}
[ -n "$RUN" ] || { echo "no successful disk build yet" >&2; exit 1; }
ssh "$HOST" "mkdir -p /root/zero-os/out && cd /root/zero-os/out && rm -f zero-os.qcow2 && \
    GH_TOKEN=$GH_TOKEN gh run download $RUN -R x0cero/zero-os --pattern '*qcow2*' --dir dl 2>&1 | tail -1; \
    find dl -name '*.qcow2' -exec mv {} zero-os.qcow2 \; ; rm -rf dl; ls -la zero-os.qcow2"
scp -q "$PROJECT_DIR/homelab/vm.sh" "$HOST:/root/zero-os/vm.sh"
ssh "$HOST" "sh /root/zero-os/vm.sh"
