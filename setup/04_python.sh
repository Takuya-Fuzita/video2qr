#!/bin/bash
set -e

source "$(dirname "$0")/common.sh"

echo "[04_python] installing python packages..."

sudo -u "${APP_USER}" "${VENV_DIR}/bin/pip" install \
    opencv-python-headless==4.13.0.92 \
    pytesseract==0.3.13 \
    qrcode==8.2 \
    numpy==2.4.4 \
    pillow==12.2.0

echo "[04_python] done"
