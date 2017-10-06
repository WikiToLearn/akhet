# Akhet

Akhet is a docker-oriented virtual-desktop environment infrastructure.

## Requirements

* Docker (linux amd64) 17.04.0-ce or greater
* `make`

## Quick start

1. Clone this repo
2. Change the working directory to this repo
3. execute `./configure` to check that al dependencies are satisfied 
4. execute `make` to build all system images
5. execute `make demoui` to build the demo UI
6. execute `make base` to build the base image
7. execute `make xterm` to build the xterm image
8. execute `./demo-run.sh`
9. open `http://localhost:8080/`

## Other make options

* plasma-base (requires base): the base plasma image
* plasma-dev (requires plasma-base): basic dev-tools with plasma UI
* plasma-science (requires plasma-dev): root6 and geant4 images with debian
* gnome-base (requires base): the base gnome image
* gnome-dev (requires gnome-base): basic dev-tools with gnome UI
* gnome-science (requires gnome-dev): root6 and geant4 images with debian
* base-cuda: base image for cuda
* xterm-cuda (requires base-cuda): xterm image with CUDA support
