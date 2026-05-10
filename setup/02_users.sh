#!/bin/bash
set -e

source "$(dirname "$0")/common.sh"

echo "[02_users] setting up user/group/venv..."

# create app user if not exists
if ! id "${APP_USER}" &>/dev/null; then
    sudo adduser --gecos "" --disabled-password "${APP_USER}"
else
    echo "[02_users] user ${APP_USER} already exists, skip"
fi

sudo usermod -aG video "${APP_USER}"

# create app group
if ! getent group "${APP_GROUP}" &>/dev/null; then
    sudo groupadd "${APP_GROUP}"
else
    echo "[02_users] group ${APP_GROUP} already exists, skip"
fi

sudo usermod -aG "${APP_GROUP}" "${APP_USER}"
sudo usermod -aG "${APP_GROUP}" admin

# venv
sudo mkdir -p "${VENV_DIR}"
sudo chown "${APP_USER}:${APP_GROUP}" "${VENV_DIR}"
sudo chmod 775 "${VENV_DIR}"

if [ ! -f "${VENV_DIR}/bin/python" ]; then
    sudo -u "${APP_USER}" python3 -m venv "${VENV_DIR}"
else
    echo "[02_users] venv already exists, skip"
fi

echo "[02_users] done"
