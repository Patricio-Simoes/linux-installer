#!/usr/bin/env bash

wget https://github.com/veracrypt/VeraCrypt/releases/download/VeraCrypt_1.26.20/veracrypt-1.26.20-Debian-12-amd64.deb
wget https://github.com/veracrypt/VeraCrypt/releases/download/VeraCrypt_1.26.20/veracrypt-1.26.20-Debian-12-amd64.deb.sig
wget https://www.idrix.fr/VeraCrypt/VeraCrypt_PGP_public_key.asc

gpg --import VeraCrypt_PGP_public_key.asc
gpg --verify veracrypt-1.26.20-Debian-12-amd64.deb.sig veracrypt-1.26.20-Debian-12-amd64.deb

if gpg --verify veracrypt-1.26.20-Debian-12-amd64.deb.sig veracrypt-1.26.20-Debian-12-amd64.deb; then
    sudo apt install -y ./veracrypt-1.26.20-Debian-12-amd64.deb
fi

rm ./veracrypt-1.26.20-Debian-12-amd64.deb
rm ./veracrypt-1.26.20-Debian-12-amd64.deb.sig
rm ./VeraCrypt_PGP_public_key.asc