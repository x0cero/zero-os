#!/bin/sh
# Runs ON the Proxmox host. Turns the published Zero OS image into a qcow2
# with bootc-image-builder (the same tool the GitHub workflow uses, which
# GitHub's runners currently refuse to give enough privileges).
set -eu
IMAGE=${1:-ghcr.io/x0cero/zero-os:latest}
OUT=/root/zero-os/bib
mkdir -p "$OUT/output" "$OUT/config"
which podman >/dev/null || (apt-get update -qq && apt-get install -y -qq podman >/dev/null)
cat > "$OUT/config/config.toml" <<TOML
[[customizations.filesystem]]
mountpoint = "/"
minsize = "20 GiB"

# A ready-made account for the test machine, so it lands on the desktop.
[[customizations.user]]
name = "zero"
password = "zero"
groups = ["wheel"]
TOML
podman pull "$IMAGE" | tail -1
podman run --rm --privileged --security-opt label=type:unconfined_t \
    -v "$OUT/output:/output" \
    -v /var/lib/containers/storage:/var/lib/containers/storage \
    -v "$OUT/config/config.toml:/config.toml:ro" \
    quay.io/centos-bootc/bootc-image-builder:latest \
    --type qcow2 --config /config.toml --use-librepo=True "$IMAGE" 2>&1 | tail -5
ls -la "$OUT/output/qcow2/disk.qcow2"
cp -f "$OUT/output/qcow2/disk.qcow2" /root/zero-os/out/zero-os.qcow2
