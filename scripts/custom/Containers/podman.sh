#!/usr/bin/env bash

# ----------------------------------------------------------------------------
# This script installs podman.
# ----------------------------------------------------------------------------

if [ "$DISTRO_ID" = "debian" ]; then
  sudo apt install -y podman
  echo "Podman installation completed successfully."
  exit 0
fi