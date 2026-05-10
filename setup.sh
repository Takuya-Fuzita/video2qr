#!/bin/bash
set -e

repoDir="$(cd "$(dirname "$0")" && pwd)"
setupDir="${repoDir}/setup"

###############
# Entry point
###############

echo "=== video2qr setup ==="
echo ""
echo "Do you need Japanese locale? (LANG=ja_JP.UTF-8  + CJK fonts)"
echo "  1) No  ( English environment )"
echo "  2) Yes ( Japanese environment ) "
echo ""

while true; do
    read -rp "> " langChoice
    case "${langChoice}" in
        1) export LANG_MODE=en; break ;;
        2) export LANG_MODE=ja; break ;;
        *) echo "Please enter 1 or 2" ;;
    esac
done

echo ""
echo "[setup] language: ${LANG_MODE}"
echo ""

bash "${setupDir}/01_packages.sh"
bash "${setupDir}/02_users.sh"
bash "${setupDir}/03_dirs.sh"
bash  "${setupDir}/04_python.sh"
bash "${setupDir}/05_system.sh"

#########
# Deploy
#########

echo "[deploy] copying source files..."
sudo cp "${repoDir}/main.py" \
        "${repoDir}/hdmi2png.py" \
        "${repoDir}/ocr2qr.py" \
        "${repoDir}/menu.json" \
        /usr/local/lib/video2qr/

sudo chmod +x /usr/local/lib/video2qr/main.py

if [ ! -L /usr/local/bin/video2qr ]; then
    sudo ln -s /usr/local/lib/video2qr/main.py /usr/local/bin/video2qr
fi

echo "[deploy] done"

bash "${setupDir}/06_autostart.sh"

echo ""
echo "=== all done. run: sudo reboot ==="
