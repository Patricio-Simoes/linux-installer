#!/usr/bin/env bash

RELEASE="1.0.8"

if [ "$DISTRO_ID" = "debian" ]; then
    #? Download the package.
    wget https://repo.protonvpn.com/debian/dists/stable/main/binary-all/protonvpn-stable-release_${RELEASE}_all.deb

    #? check the repo package’s integrity.
    INTEGRITY=$(echo "0b14e71586b22e498eb20926c48c7b434b751149b1f2af9902ef1cfe6b03e180 protonvpn-stable-release_${RELEASE}_all.deb" | sha256sum --check -)

    if [[ $? -eq 0 ]]; then
        echo "Pronton VPN's repository checksum validation was successful."
    else
        echo "Pronton VPN's repository checksum validation failed."
        exit 1
    fi

    #? Install the Proton VPN repository.
    sudo dpkg -i ./protonvpn-stable-release_${RELEASE}_all.deb && sudo apt update

    #? Install the app.
    sudo apt install proton-vpn-gnome-desktop -y

    #? Clean up.
    rm ./protonvpn-stable-release_${RELEASE}_all.deb
fi