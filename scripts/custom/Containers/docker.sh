#!/usr/bin/env bash

# ----------------------------------------------------------------------------
# This script installs and configures Docker. It removes old versions,
# sets up the Docker repository, installs Docker and its components,
# and configures the system to enable Docker usage.
# ----------------------------------------------------------------------------

if [ "$DISTRO_ID" = "debian" ]; then
  #? Uninstall old versions.
  for pkg in docker.io docker-compose docker-doc podman-docker containerd runc; do
      if dpkg -l | grep -q "$pkg"; then
          echo "Removing $pkg..."
          sudo apt remove -y "$pkg"
      else
          echo "$pkg is not installed."
      fi
  done

  #? Install Docker using the apt repository.
  sudo apt update
  sudo apt install -y ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings

  #? Add Docker’s official GPG key.
  sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc

  #? Add the repository to Apt sources.
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  #? Install Docker and its components.
  sudo apt update
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

  #? Start Docker and enable on boot.
  sudo systemctl start docker
  sudo systemctl enable docker
  sudo systemctl status docker

  #? Add user to docker group.
  sudo groupadd docker
  sudo usermod -aG docker $USER
  
  sudo systemctl restart docker

  echo "Docker installation and configuration completed successfully."
  exit 0
fi