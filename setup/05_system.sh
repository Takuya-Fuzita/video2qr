#!/bin/bash
set -e

source "$(dirname "$0")/common.sh"

echo "[05_system] configuring sudoers / systemd / udev..."

######
# sudoers
######

sudoersFile=/etc/sudoers.d/video2qr
echo "${APP_USER} ALL=(ALL) NOPASSWD: /usr/sbin/shutdown" | sudo tee "${sudoersFile}" > /dev/null
sudo chmod 0440 "${sudoersFile}"
sudo visudo -c

###########
# systemd - autologin on tty1
###########

overrideDir=/etc/systemd/system/getty@tty1.service.d
sudo mkdir -p "${overrideDir}"

sudo tee "${overrideDir}/override.conf" > /dev/null << EOF
[Service]
ExecStart=
ExecStart=-/usr/sbin/agetty --autologin ${APP_USER} --noclear %I \$TERM
EOF

########
# udev - fix card0/card1 swap issue
########

sudo tee /etc/udev/rules.d/99-drm-hdmi.rules > /dev/null << 'EOF'
SUBSYSTEM=="drm", ENV{ID_PATH}=="platform-gpu", SYMLINK+="dri/hdmi-card"
EOF

sudo udevadm control --reload-rules
sudo udevadm trigger

echo "[05_system] done"
