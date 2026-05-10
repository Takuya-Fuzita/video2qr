#!/bin/bash
set -e

source "$(dirname "$0")/common.sh"

echo "[03_dirs] creating directories..."

sudo install -d -m 775 -o "${APP_USER}" -g "${APP_GROUP}" "${LOG_DIR}"
sudo install -d -m 775 -o "${APP_USER}" -g "${APP_GROUP}" "${SAVE_DIR}"
sudo install -d -m 775 -o "${APP_USER}" -g "${APP_GROUP}" "${LIB_DIR}"

echo "[03_dirs] done"
