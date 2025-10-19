#!/usr/bin/env bash

if [ "$DISTRO_ID" = "debian" ]; then
    #? Install Prerequisites and Detect GPU.
    sudo apt install -y linux-headers-$(uname -r) build-essential dkms nvidia-detect
    if [ $? -ne 0 ]; then
        echo "Failed to install NVIDIA prerequisites."
        exit 1
    fi

    nvidia-detect
    if [ $? -ne 0 ]; then
        echo "Failed to detect NVIDIA GPU."
        exit 1
    fi

    #? Install NVIDIA Driver Package
    sudo apt install -y nvidia-driver nvidia-kernel-dkms -y
    if [ $? -ne 0 ]; then
        echo "Failed to install NVIDIA driver package."
        exit 1
    fi

    echo "All NVIDIA installations were successful."
    exit 0
fi