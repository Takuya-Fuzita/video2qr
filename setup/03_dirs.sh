#!/bin/bash
set -e

source "$(dirname "$0")/common.sh"

echo "[03_dirs] creating directories..."

sudo install -d -o "${APP_USER}" -g "${APP_USER}" "${LOG_DIR}"
sudo install -d -o "${APP_USER}" -g "${APP_USER}" "${SAVE_DIR}"
sudo install -d -o "${APP_USER}" -g "${APP_USER}" "${LIB_DIR}"

echo "[03_dirs] done"
