#!/usr/bin/env bash

# ----------------------------------------------------------------------------
# This script installs veracrypt using the official packages at https://veracrypt.io/en/Downloads.html.
# ----------------------------------------------------------------------------

if [ "$DISTRO_ID" = "debian" ]; then
    DEBIAN_VERSION="13"
    VERACRYPT_VERSION="1.26.24"
    wget https://github.com/veracrypt/VeraCrypt/releases/download/VeraCrypt_${VERACRYPT_VERSION}/veracrypt-${VERACRYPT_VERSION}-Debian-${DEBIAN_VERSION}-amd64.deb
    wget https://github.com/veracrypt/VeraCrypt/releases/download/VeraCrypt_${VERACRYPT_VERSION}/veracrypt-${VERACRYPT_VERSION}-Debian-${DEBIAN_VERSION}-amd64.deb.sig
    wget https://www.idrix.fr/VeraCrypt/VeraCrypt_PGP_public_key.asc

    gpg --import VeraCrypt_PGP_public_key.asc
    gpg --verify veracrypt-${VERACRYPT_VERSION}-Debian-${DEBIAN_VERSION}-amd64.deb.sig veracrypt-${VERACRYPT_VERSION}-Debian-${DEBIAN_VERSION}-amd64.deb

    if gpg --verify veracrypt-${VERACRYPT_VERSION}-Debian-${DEBIAN_VERSION}-amd64.deb.sig veracrypt-${VERACRYPT_VERSION}-Debian-${DEBIAN_VERSION}-amd64.deb; then
        sudo apt install -y ./veracrypt-${VERACRYPT_VERSION}-Debian-${DEBIAN_VERSION}-amd64.deb

        #? Cleanup.
        rm ./veracrypt-${VERACRYPT_VERSION}-Debian-${DEBIAN_VERSION}-amd64.deb
        rm ./veracrypt-${VERACRYPT_VERSION}-Debian-${DEBIAN_VERSION}-amd64.deb.sig
        rm ./VeraCrypt_PGP_public_key.asc

        echo "VeraCrypt installed successfully."
        exit 0
    fi

    echo "VeraCrypt package verification failed. Aborting installation."
    exit 1

    #? Cleanup.
    rm ./veracrypt-${VERACRYPT_VERSION}-Debian-${DEBIAN_VERSION}-amd64.deb
    rm ./veracrypt-${VERACRYPT_VERSION}-Debian-${DEBIAN_VERSION}-amd64.deb.sig
    rm ./VeraCrypt_PGP_public_key.asc
fi
