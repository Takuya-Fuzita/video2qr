#!/bin/bash

source "$(dirname "$0")/common.sh"

#########
# helpers
#########

ok=0
ng=0

funcCheck() {
    local targetPath="$1"
    if [ -e "${targetPath}" ] || [ -L "${targetPath}" ]; then
        echo "[OK] $(ls -la "${targetPath}")"
        ok=$((ok + 1))
    else
        echo "[NG] NOT FOUND: ${targetPath}"
        ng=$((ng + 1))
    fi
}

##########
# checks
##########

echo "=== verify ==="
echo ""

echo "--- sudoers ---"
funcCheck /etc/sudoers.d/video2qr

echo ""
echo "--- systemd ---"
funcCheck /etc/systemd/system/getty@tty1.service.d/override.conf

echo ""
echo "--- udev ---"
funcCheck /etc/udev/rules.d/99-drm-hdmi.rules
funcCheck /dev/dri/hdmi-card

echo ""
echo "--- app files ---"
funcCheck "${LIB_DIR}/main.py"
funcCheck "${LIB_DIR}/hdmi2png.py"
funcCheck "${LIB_DIR}/ocr2qr.py"
funcCheck "${LIB_DIR}/menu.json"
funcCheck "${BIN_LINK}"

echo ""
echo "--- venv ---"
funcCheck "${VENV_DIR}/bin/python"
funcCheck "${VENV_DIR}/bin/pip"

echo ""
echo "--- directories ---"
funcCheck "${SAVE_DIR}"
funcCheck "${LOG_DIR}"
funcCheck "${LIB_DIR}"

echo ""
echo "--- autostart ---"
funcCheck "/home/${APP_USER}/.bash_profile"

echo ""
echo "=== result: ${ok} ok / ${ng} ng ==="
