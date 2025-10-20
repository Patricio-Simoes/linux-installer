#!/usr/bin/env bash

# ----------------------------------------------------------------------------
# This script configures the ZRAM swap settings for a Debian-based system.
# It updates the ZRAM configuration file with specified values for compression
# algorithm, memory percentage, size, and priority. The script also creates a
# backup of the original configuration file before making changes.

# Variables:
#   ALGO: Compression algorithm to use for ZRAM (e.g., lz4, zstd).
#   PERCENT: Percentage of total memory to allocate for ZRAM.
#   SIZE: Fixed size (in MB) to allocate for ZRAM, if not using percentage.
#   PRIORITY: Priority level of the ZRAM swap device.

# Behavior:
#   - Checks if the system's distribution ID is "debian".
#   - Creates a backup of the ZRAM configuration file at /etc/default/zramswap.
#   - Updates the configuration file with the specified values.
#   - Ensures the configuration file has appropriate permissions.
#   - Exits with a success message upon completion.
# ----------------------------------------------------------------------------

ALGO="lz4"
PERCENT=10
SIZE=256
PRIORITY=100

if [ "$DISTRO_ID" = "debian" ]; then
    ZRAMSWAP_FILE="/etc/default/zramswap"

    #? Backup the original file.
    sudo cp "$ZRAMSWAP_FILE" "${ZRAMSWAP_FILE}.bak"
    echo "zram backup created at ${ZRAMSWAP_FILE}.bak"

    #? Update the ALGO, PERCENT, SIZE, and PRIORITY values
    sudo sed -i "s/^#*ALGO=.*/ALGO=$ALGO/" "$ZRAMSWAP_FILE"
    sudo sed -i "s/^#*PERCENT=.*/PERCENT=$PERCENT/" "$ZRAMSWAP_FILE"
    sudo sed -i "s/^#*SIZE=.*/SIZE=$SIZE/" "$ZRAMSWAP_FILE"
    sudo sed -i "s/^#*PRIORITY=.*/PRIORITY=$PRIORITY/" "$ZRAMSWAP_FILE"

    #? Set the appropriate permissions on the file
    chmod 644 "$ZRAMSWAP_FILE"

    echo "Successfully updated $ZRAMSWAP_FILE."
    exit 0
fi