#!/usr/bin/env bash

if [ "$DISTRO_ID" = "debian" ]; then
    #? Check if ufw is installed.
    if ! dpkg -l | grep -q ufw; then
        sudo apt install ufw -y
    fi
    #? Check if ufw is already enabled
    if ! sudo ufw status | grep -q "active"; then
        sudo ufw enable
        sudo ufw default deny incoming
        sudo ufw default allow outgoing
    fi
    sudo ufw status verbose
fi