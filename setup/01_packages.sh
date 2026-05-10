#!/bin/bash
set -e

# echo "[01_packages] apt update..."
# sudo apt update
# sudo apt upgrade -y

echo "[01_packages] installing packages..."
# sudo apt install -y git
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y tesseract-ocr
sudo apt install -y fbi
sudo apt install -y libgl1 libglib2.0-0
sudo apt install -y fbterm
if [ "${LANG_MODE}" = "ja" ]; then
    sudo apt install -y fonts-noto-cjk
fi
sudo apt install  -y vim

echo "[01_packages] done"
