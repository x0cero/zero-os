# Zero OS

A desktop Linux with its own look, built the way Bazzite and Bluefin are
built: a Fedora Atomic image on top of Universal Blue's Aurora (KDE Plasma),
assembled by GitHub from this repository, signed, and delivered as an
installer ISO with automatic updates.

The look is the one people already know from a Mac, done properly on Linux
and then made better: a menu bar along the top, a dock along the bottom,
translucent panels, rounded windows with the three buttons on the left, one
typeface everywhere, and nothing on screen that does not need to be there.

## Try it

From any bootc system (Bazzite, Bluefin, Aurora, Fedora Atomic):

    sudo bootc switch ghcr.io/x0cero/zero-os:latest

Or install from the ISO produced by the "Build disk images" workflow.

## Layout

- `Containerfile`: the base image and the one build step.
- `build_files/build.sh`: packages and system changes.
- `system_files/`: files copied onto the image as-is (the defaults live here).
- `disk_config/`: the ISO and disk image settings.

Built from [ublue-os/image-template](https://github.com/ublue-os/image-template).
