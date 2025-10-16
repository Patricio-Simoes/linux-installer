#!/usr/bin/env bash

sudo apt update

# Required dependencies.
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings

# Add Docker’s official GPG key.
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Set up the Docker repository.
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker and its components.

sudo apt update

sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start Docker and enable on boot.

sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl status docker

# Add user to docker group.

sudo groupadd docker
sudo usermod -aG docker $USER
