# Cloud Agent base image for TheRock (ROCm/HIP build super-project).
#
# Provides the stable system toolchain and a shared Python virtual environment.
# Repository-specific Python dependencies are installed by .cursor/install.sh
# after the source tree is checked out.
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# System build dependencies. This mirrors the Ubuntu 24.04 package list from the
# project README ("Building from source" -> "Setup - Ubuntu (24.04)") plus git
# and curl, which fully custom images must provide.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        automake \
        bison \
        ca-certificates \
        cmake \
        curl \
        flex \
        g++ \
        gcc \
        gfortran \
        git \
        libegl1-mesa-dev \
        libtool \
        make \
        ninja-build \
        pkg-config \
        python3 \
        python3-dev \
        python3-venv \
        sudo \
        texinfo \
        xxd \
    && rm -rf /var/lib/apt/lists/*

# The ubuntu:24.04 image ships an "ubuntu" user at uid 1000; create it only if
# it is missing and grant passwordless sudo for interactive setup.
RUN if ! id ubuntu >/dev/null 2>&1; then \
        useradd --create-home --shell /bin/bash --uid 1000 ubuntu; \
    fi \
    && echo "ubuntu ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ubuntu \
    && chmod 0440 /etc/sudoers.d/ubuntu

# Shared virtual environment placed on PATH so every boot and every shell uses
# the same interpreter without needing to activate it manually. Populated by
# .cursor/install.sh once the repository is available.
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/python -m pip install --upgrade pip \
    && chown -R ubuntu:ubuntu /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH=/opt/venv/bin:$PATH

# Also expose the venv to interactive login shells that may not inherit the
# image ENV (Cloud Agent terminals), so `python`/`pip` resolve without manual
# activation.
RUN printf 'export VIRTUAL_ENV=/opt/venv\nexport PATH=/opt/venv/bin:$PATH\n' \
        > /etc/profile.d/therock-venv.sh

USER ubuntu
