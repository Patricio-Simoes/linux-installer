#!/usr/bin/env bash

# ----------------------------------------------------------------------------
# This script installs distrobox using the official install script.
# ----------------------------------------------------------------------------

if [ "$DISTRO_ID" = "debian" ]; then
  #? New shell is required if backend is docker, due to current one
  #? not having docker permissions if installing both docker & distrobox at the same time.
  if getent group docker > /dev/null; then
    newgrp docker bash -c "curl -s https://raw.githubusercontent.com/89luca89/distrobox/main/install | sh"
  else
    #? Native package already uses podman.
    sudo apt install distrobox -y
  fi
  exit 0
fi