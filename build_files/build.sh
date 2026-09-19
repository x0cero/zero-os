#!/bin/bash

set -ouex pipefail

# Copy the contents of system_files/ of the git repo to /
cp -avf "/ctx/system_files"/. /

### Packages
# xcursorgen turns the painted cursor frames into a cursor theme.
dnf5 install -y xcursorgen

### The pictures: wallpaper, cursor, mark. Painted at build time in ink on
### paper by build_files/paint.py, which needs nothing but Python.
PAINT=/tmp/zero-paint
python3 /ctx/paint.py "$PAINT"

install -Dm644 "$PAINT/wallpaper/zero-paper.png" /usr/share/wallpapers/ZeroPaper/contents/images/2560x1600.png
install -Dm644 "$PAINT/wallpaper/zero-paper.png" /usr/share/backgrounds/zero-paper.png

install -Dm644 "$PAINT/mark/zero-mark-256.png" /usr/share/icons/hicolor/256x256/apps/zero-os.png
install -Dm644 "$PAINT/mark/zero-mark-64.png" /usr/share/icons/hicolor/64x64/apps/zero-os.png
install -Dm644 "$PAINT/mark/zero-mark-256.png" /usr/share/pixmaps/zero-os.png

# The cursor theme: every shape is the arrow except the text beam. Names
# other programs ask for point at the same files.
CURSORS=/usr/share/icons/ZeroInk/cursors
mkdir -p "$CURSORS"
for shape in left_ptr xterm hand2; do
    (cd "$PAINT/cursor" && xcursorgen "$shape.cursor" "$CURSORS/$shape")
done
for alias in default arrow top_left_arrow pointer context-menu help progress wait watch \
    left_ptr_watch dnd-move dnd-copy dnd-link move all-scroll grabbing crosshair cell \
    col-resize row-resize ew-resize ns-resize nesw-resize nwse-resize n-resize s-resize \
    e-resize w-resize ne-resize nw-resize se-resize sw-resize size_ver size_hor size_bdiag \
    size_fdiag fleur not-allowed no-drop zoom-in zoom-out openhand closedhand; do
    ln -sf left_ptr "$CURSORS/$alias"
done
for alias in text ibeam vertical-text; do
    ln -sf xterm "$CURSORS/$alias"
done
for alias in pointing_hand hand1 hand grab; do
    ln -sf hand2 "$CURSORS/$alias"
done

fc-cache -f
gtk-update-icon-cache -f /usr/share/icons/hicolor || true
