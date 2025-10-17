#!/usr/bin/env bash

# ----------------------------------------------------------------------------
# This script updates the system's DNS configuration by modifying the
# /etc/resolv.conf file. It allows you to select a DNS server from a predefined
# list (Cloudflare, Quad9, Google), adds the corresponding nameserver entries
# to /etc/resolv.conf, and then makes the file immutable to prevent further changes.
#
# Usage:
# ./dns.sh <DNS_SERVER>
#
# <DNS_SERVER> is one of the following options:
#   - Cloudflare: 1.1.1.1 1.0.0.1
#   - Quad9: 9.9.9.9 149.112.112.112
#   - Google: 8.8.8.8 8.8.4.4
# ----------------------------------------------------------------------------

declare -A SERVERS

SERVERS["Cloudflare"]="1.1.1.1 1.0.0.1"
SERVERS["Quad9"]="9.9.9.9 149.112.112.112"
SERVERS["Google"]="8.8.8.8 8.8.4.4"

DNS_SERVER=$1

if [[ -f '/etc/resolv.conf' ]]; then 
    sudo chattr -i /etc/resolv.conf
    sudo rm /etc/resolv.conf
    sudo touch /etc/resolv.conf
fi

for ip in ${SERVERS[$DNS_SERVER]}; do
    echo "nameserver $ip" | sudo tee -a /etc/resolv.conf > /dev/null
    if [[ $? -ne 0 ]]; then
        echo "Failed to add nameserver $ip"
        exit 1
    fi
done

sudo chattr +i /etc/resolv.conf
if [[ $? -ne 0 ]]; then
    echo "Failed to make resolv.conf immutable"
    exit 1
fi

echo "DNS servers updated successfully"
exit 0
