#!/usr/bin/env sh

# variables
GIT_REF=${1}
GIT_DIR=${2}
PUID=${3}
PGID=${4}

# log date
date

# install git
if ! command -v git > /dev/null 2>&1; then
    apk add --no-cache \
        git
fi

# install openssh
if ! command -v ssh > /dev/null 2>&1; then
    apk add --no-cache \
        openssh
fi

# allow git with different ownership
git config --global --add safe.directory ${GIT_DIR}

# fetch from git
git fetch --all

# checkout git reference
git checkout --force ${GIT_REF}

# set ownership
chown -R ${PUID}:${PGID} ${GIT_DIR}