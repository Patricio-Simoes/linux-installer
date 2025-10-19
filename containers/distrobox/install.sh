#!/usr/bin/env bash

# ----------------------------------------------------------------------------
# This script is used to create a container using distrobox. 
# It takes the container name as an argument, navigates to the appropriate directory, 
# and runs the `distrobox assemble create` command to set up the container.
# ----------------------------------------------------------------------------

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTAINER_NAME="$1"

if [ -z "$CONTAINER_NAME" ]; then
    echo "Error: No container name provided. Please provide a container name as an argument."
    exit 1
fi

cd ${CURRENT_DIR}/${CONTAINER_NAME}

#? New shell is required if backend is docker, due to current one
#? not having docker permissions if installing both docker & distrobox at the same time.
if getent group docker > /dev/null; then
    newgrp docker bash -c "${HOME}/.local/bin/distrobox-assemble create"
else
    distrobox-assemble create
fi

#? Check if the command was successful
if [ $? -eq 0 ]; then
    echo "${CONTAINER_NAME} assemble create was successful."
    cd $SCRIPT_DIR
    exit 0
else
    echo "${CONTAINER_NAME} assemble create failed."
    cd $SCRIPT_DIR
    exit 1
fi
