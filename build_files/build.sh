#!/bin/bash

set -ouex pipefail

# Copy the contents of system_files/ of the git repo to /
cp -avf "/ctx/system_files"/. /

### Packages
# Kvantum draws the widgets; Inter and JetBrains Mono are the system fonts;
# the app menu applet puts the focused program's menus in the top bar.
dnf5 install -y kvantum rsms-inter-fonts jetbrains-mono-fonts plasma-workspace-appmenu 2>/dev/null \
    || dnf5 install -y kvantum rsms-inter-fonts jetbrains-mono-fonts

### The look: the WhiteSur family (GPL-3.0), installed system-wide.
# Window decoration, Plasma theme, colour scheme and Kvantum theme.
WORK=/tmp/zero-look
mkdir -p "$WORK"
curl -sL https://github.com/vinceliuice/WhiteSur-kde/archive/refs/heads/master.tar.gz | tar xz -C "$WORK"
(cd "$WORK/WhiteSur-kde-master" && ./install.sh --color light --window default)
# Icons, with KDE's logo in place of the fruit, since that one is not ours to ship.
curl -sL https://github.com/vinceliuice/WhiteSur-icon-theme/archive/refs/heads/master.tar.gz | tar xz -C "$WORK"
(cd "$WORK/WhiteSur-icon-theme-master" && ./install.sh --kde-plasma --dest /usr/share/icons)
# Cursors.
curl -sL https://github.com/vinceliuice/WhiteSur-cursors/archive/refs/heads/master.tar.gz | tar xz -C "$WORK"
(cd "$WORK/WhiteSur-cursors-master" && ./install.sh)
rm -rf "$WORK"

### The pictures: wallpaper and mark, painted by build_files/paint.py.
PAINT=/tmp/zero-paint
python3 /ctx/paint.py "$PAINT"
install -Dm644 "$PAINT/wallpaper/zero.png" /usr/share/wallpapers/Zero/contents/images/2560x1600.png
install -Dm644 "$PAINT/wallpaper/zero.png" /usr/share/backgrounds/zero.png
for size in 16 22 24 32 48 64 128 256; do
    install -Dm644 "$PAINT/mark/zero-mark-$size.png" "/usr/share/icons/hicolor/${size}x${size}/apps/zero-os.png"
    # The top bar is light, so the mark on it is dark; the same file serves both
    # the hicolor set and the WhiteSur set so the launcher finds it either way.
    install -Dm644 "$PAINT/mark/zero-mark-$size.png" "/usr/share/icons/WhiteSur/apps/scalable/zero-os.png" 2>/dev/null || true
done
install -Dm644 "$PAINT/mark/zero-mark-256.png" /usr/share/pixmaps/zero-os.png
rm -rf "$PAINT"

### No first-run wizard: the installer already made the account.
systemctl mask plasma-setup.service || true

fc-cache -f
gtk-update-icon-cache -f /usr/share/icons/hicolor || true
