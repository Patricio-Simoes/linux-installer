#!/usr/bin/env bash

export SUPPORTED_DISTROS=("debian")

exit() {
    echo "$1"
    command exit 0 
}

check_and_source_file() {
    local SOURCE_FILE=${1}

    if [[ -f "$SOURCE_FILE" ]]; then
        source "$SOURCE_FILE"
    else
        echo "Error: $SOURCE_FILE not found." >&2
        exit 1
    fi
}

#? Directory of the current, (init.sh), script.
export SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export LOG_DIR="$SCRIPT_DIR/logs"

chmod 700 "$SCRIPT_DIR/scripts/custom/"*.sh
chmod 700 "$SCRIPT_DIR/scripts/custom/VPNs/"*.sh
chmod 700 "$SCRIPT_DIR/scripts/custom/Firewalls/"*.sh

#? Determine the distro the user is using.
if [ -f /etc/os-release ];then
    export DISTRO_ID=$(grep '^ID=' /etc/os-release | cut -d'=' -f2 | tr -d '"')
    mkdir -p "$LOG_DIR"
    if [[ " ${SUPPORTED_DISTROS[@]} " =~ " $DISTRO_ID " ]]; then
        sudo apt install python -y > /dev/null 2>&1
    else
        exit "Distro $DISTRO_ID is not supported. Supported distros are: ${SUPPORTED_DISTROS[*]}"
    fi
    python3 "$SCRIPT_DIR/scripts/main/main.py"
else
    exit "Could not determine distro."
fi
