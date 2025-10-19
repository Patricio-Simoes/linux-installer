#!/usr/bin/env bash

if [ "$DISTRO_ID" = "debian" ]; then
    sudo apt install -y qemu-kvm qemu-guest-agent libvirt-daemon libvirt-clients bridge-utils virt-manager

    sudo systemctl enable --now libvirtd
    
    sudo virsh net-start default
    sudo virsh net-autostart default

    sudo usermod -aG libvirt $USER
    sudo usermod -aG libvirt-qemu $USER
    sudo usermod -aG kvm $USER
    sudo usermod -aG input $USER
    sudo usermod -aG disk $USER
fi