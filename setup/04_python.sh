#!/bin/bash
set -e

source "$(dirname "$0")/common.sh"

echo "[04_python] installing python packages..."

sudo -u "${APP_USER}" "${VENV_DIR}/bin/pip" install \
    opencv-python-headless \
    pytesseract \
    qrcode \
    numpy \
    Pillow

echo "[04_python] done"
