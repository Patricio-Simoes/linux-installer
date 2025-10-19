#!/usr/bin/env bash

export SUPPORTED_DISTROS=("debian")

check_and_source_file() {
    local SOURCE_FILE=${1}

    if [[ -f "$SOURCE_FILE" ]]; then
        source "$SOURCE_FILE"
    else
        echo "Error: $SOURCE_FILE not found."
        exit 1
    fi
}

#? Directory of the current, (init.sh), script.
export SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export LOG_DIR="$SCRIPT_DIR/logs"

chmod 700 "$SCRIPT_DIR/scripts/custom/Containers/"*.sh
chmod 700 "$SCRIPT_DIR/containers/distrobox/install.sh"
chmod 700 "$SCRIPT_DIR/scripts/custom/Firewalls/"*.sh
chmod 700 "$SCRIPT_DIR/scripts/custom/System_Utilities/"*.sh
chmod 700 "$SCRIPT_DIR/scripts/custom/VPNs/"*.sh

 mkdir -p "$LOG_DIR"

#? Determine the distro the user is using.
if [ -f /etc/os-release ];then
    export DISTRO_ID=$(grep '^ID=' /etc/os-release | cut -d'=' -f2 | tr -d '"')
else
    echo "Could not determine distro."
    exit 1
fi

if [[ " ${SUPPORTED_DISTROS[@]} " =~ " $DISTRO_ID " ]]; then
    if [ "$DISTRO_ID" == "debian" ]; then
        #? Install Python if not yet installed.
        command -v python3 >/dev/null 2>&1 || sudo apt install python3 -y
        #? Enable contrib & non-free repos for Debian.
        sudo sed -i 's/main/main non-free contrib/g' /etc/apt/sources.list
    fi
else
    exit "Distro $DISTRO_ID is not supported. Supported distros are: ${SUPPORTED_DISTROS[*]}"
fi
python3 "$SCRIPT_DIR/scripts/main/main.py"
