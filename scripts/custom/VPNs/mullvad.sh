#!/usr/bin/env bash

if [ "$DISTRO_ID" = "debian" ]; then
    #? Download Mullvad's signing key.
    sudo curl -fsSLo /usr/share/keyrings/mullvad-keyring.asc https://repository.mullvad.net/deb/mullvad-keyring.asc

    #?  Add the stable repository.
    echo "deb [signed-by=/usr/share/keyrings/mullvad-keyring.asc arch=$( dpkg --print-architecture )] https://repository.mullvad.net/deb/stable stable main" | sudo tee /etc/apt/sources.list.d/mullvad.list

    #? Install the package.
    sudo apt update && sudo apt install mullvad-vpn
fi