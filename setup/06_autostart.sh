#!/bin/bash
set -e

source "$(dirname "$0")/common.sh"

echo "[06_autostart] writing .bash_profile for ${APP_USER}..."

bashProfile="/home/${APP_USER}/.bash_profile"

# skip if already written
if sudo -u "${APP_USER}" grep -q "video2qr" "${bashProfile}" 2>/dev/null; then
    echo "[06_autostart] already configured, skip"
    exit 0
fi

sudo -u "${APP_USER}" tee -a "${bashProfile}" > /dev/null << 'BASHEOF'

if [ "$(tty)" = "/dev/tty1" ]; then
    export TERM=fbterm
BASHEOF

if [ "${LANG_MODE}" = "ja" ]; then
    sudo -u "${APP_USER}" tee -a "${bashProfile}" > /dev/null << 'BASHEOF'
    export LANG=ja_JP.UTF-8
BASHEOF
fi

sudo -u "${APP_USER}" tee -a "${bashProfile}" > /dev/null << 'BASHEOF'
    fbterm -s 48 -- /usr/local/bin/video2qr
fi
BASHEOF

echo "[06_autostart] done"
