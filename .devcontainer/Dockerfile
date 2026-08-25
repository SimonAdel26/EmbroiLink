# syntax=docker/dockerfile:1

FROM ubuntu:24.04
RUN apt-get update \
    && apt-get install -y \
        git \
        python3 \
        python3-pip \
        curl \
        libgl1 libegl1 libglib2.0-0 \
        libxcb-cursor0 libxcb-xinerama0 libxcb-icccm4 libxcb-image0 \
        libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 \
        libxkbcommon-x11-0 libdbus-1-3 libfontconfig1 \
        qt6-wayland \
    && rm -rf /var/lib/apt/lists/*

