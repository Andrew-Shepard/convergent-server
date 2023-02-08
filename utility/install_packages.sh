#!/bin/bash
# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get -y upgrade

# install without junk
apt-get -y install --no-install-recommends \
    bash \
    curl \
    libxslt-dev \
    vim \
    ca-certificates \
    libpq-dev \
    gcc \
    nginx xz-utils \
    netcat

pip3 install \
    envtpl==0.6.0 \
    jinja2==2.10.3 \
    markupsafe==1.1.1

# purge cache
apt-get clean
rm -rf /var/lib/apt/lists/*
