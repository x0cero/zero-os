# Zero OS

A desktop Linux with its own look, built the way Bazzite and Bluefin are
built: a Fedora Atomic image on top of Universal Blue's Aurora (KDE Plasma),
assembled by GitHub from this repository, signed, and delivered as an
installer ISO with automatic updates.

The look is the newsprint machine: black ink on paper, no grey, chunky pixel
type where it counts, hard shadows, and motion with momentum, finished to the
standard people expect from a Mac.

## Try it

From any bootc system (Bazzite, Bluefin, Aurora, Fedora Atomic):

    sudo bootc switch ghcr.io/x0cero/zero-os:latest

Or install from the ISO produced by the "Build disk images" workflow.

## Layout

- `Containerfile`: the base image and the one build step.
- `build_files/build.sh`: packages and system changes.
- `system_files/`: files copied onto the image as-is (the theme lives here).
- `disk_config/`: the ISO and disk image settings.

Built from [ublue-os/image-template](https://github.com/ublue-os/image-template).
