#!/bin/sh
# Runs ON the Proxmox host. Boots a Zero OS qcow2 (from the "Build disk
# images" workflow) as VM 303, replacing the disk if the VM exists.
set -eu
VMID=${1:-303}
IMAGE=${2:-/root/zero-os/out/zero-os.qcow2}
[ -f "$IMAGE" ] || { echo "no image at $IMAGE" >&2; exit 1; }

if qm status "$VMID" >/dev/null 2>&1; then
    qm stop "$VMID" >/dev/null 2>&1 || true
    qm set "$VMID" --delete virtio0 >/dev/null 2>&1 || true
    for u in $(qm config "$VMID" | sed -n 's/^\(unused[0-9]*\):.*/\1/p'); do
        qm disk unlink "$VMID" --idlist "$u" --force >/dev/null 2>&1 || true
    done
else
    qm create "$VMID" --name zero-os --machine q35 --bios ovmf \
        --efidisk0 local-lvm:1,efitype=4m,pre-enrolled-keys=0 \
        --memory 6144 --balloon 0 --cores 4 --cpu host \
        --vga virtio --net0 virtio,bridge=vmbr0 --ostype l26 --tablet 1 \
        --agent 1 --scsihw virtio-scsi-pci --onboot 0 >/dev/null
fi

VOL=$(qm importdisk "$VMID" "$IMAGE" local-lvm 2>/dev/null \
    | sed -n "s/.*imported disk '\([^']*\)'.*/\1/p")
[ -n "$VOL" ] || { echo "disk import failed" >&2; exit 1; }
qm set "$VMID" --virtio0 "$VOL" --boot order=virtio0 >/dev/null
qm resize "$VMID" virtio0 40G >/dev/null 2>&1 || true
qm start "$VMID"
echo "Started VM $VMID from $IMAGE"
