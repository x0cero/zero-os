#!/bin/sh
# Runs ON the Proxmox host. Types a line into a VM's console through the
# QEMU monitor, one key at a time, then presses Return.
#   sh type.sh 303 "sudo systemctl disable plasma-setup"
set -eu
VMID=$1
TEXT=$2
last=""
key() {
    # The same key twice in a row needs a pause or the console sees a hold.
    if [ "$1" = "$last" ]; then sleep 0.3; fi
    qm sendkey "$VMID" "$1" >/dev/null
    last=$1
    sleep 0.08
}
for hex in $(printf '%s' "$TEXT" | od -An -tx1 | tr -s ' \n' '  '); do
    case "$hex" in
        20) key spc ;; 2d) key minus ;; 3d) key equal ;; 2f) key slash ;;
        2e) key dot ;; 2c) key comma ;; 3b) key semicolon ;; 27) key apostrophe ;;
        5b) key bracket_left ;; 5d) key bracket_right ;; 5c) key backslash ;;
        60) key grave_accent ;;
        5f) key shift-minus ;; 2b) key shift-equal ;; 3a) key shift-semicolon ;;
        7c) key shift-backslash ;; 3e) key shift-dot ;; 3c) key shift-comma ;;
        22) key shift-apostrophe ;; 7e) key shift-grave_accent ;;
        21) key shift-1 ;; 40) key shift-2 ;; 23) key shift-3 ;; 24) key shift-4 ;;
        25) key shift-5 ;; 5e) key shift-6 ;; 26) key shift-7 ;; 2a) key shift-8 ;;
        28) key shift-9 ;; 29) key shift-0 ;;
        7b) key shift-bracket_left ;; 7d) key shift-bracket_right ;;
        3[0-9]) key "$(printf "\\$(printf '%03o' 0x$hex)")" ;;
        4[1-9]|4[a-f]|5[0-9a]) key "shift-$(printf "\\$(printf '%03o' 0x$hex)" | tr 'A-Z' 'a-z')" ;;
        6[1-9]|6[a-f]|7[0-9a]) key "$(printf "\\$(printf '%03o' 0x$hex)")" ;;
        *) ;;
    esac
done
key ret
