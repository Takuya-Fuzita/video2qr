#!/opt/venv/video2qr/bin/python

import os
import sys
import json
import logging
import termios
import tty
import subprocess
import shutil
from datetime import datetime

import hdmi2png
import ocr2qr

#########
# Constants
#########

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

SAVE_DIR  = "/var/opt/pics"
LOG_FILE = "/var/log/myapps/hdmi2qr.log"
MENU_JSON = os.path.join(SCRIPT_DIR, "menu.json")
VIDEO_DEVICE_INDEX = 0

SHELL_SEQUENCE = "!shell!"
EXIT_SEQUENCE = "!exit!"

###########
# Logging
###########

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console = logging.StreamHandler()
console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logging.getLogger().addHandler(console)
logging.getLogger("pytesseract").setLevel(logging.WARNING)
logger = logging.getLogger("main")

##############
# Helper funcs
##############

def funcReadKey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch


def funcLoadMenu():
    with open(MENU_JSON, encoding="utf-8") as f:
        data = json.load(f)
    return data["menu_items"]


def execShowMenu(menuItems):
    os.system("clear")
    print("================================")
    print("  HDMI Capture Menu")
    print("================================")
    print("")
    for i, item in enumerate(menuItems, start=1):
        print(f"  {i}    {item['label']}")
    print("")
    print("  0    Shutdown")
    print("")
    print("================================")


def execRunCapture(item):
    print("")
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
    outputPath = os.path.join(SAVE_DIR, filename)

    try:
        logger.info(f"capture start: {outputPath}")
        hdmi2png.execCapture(outputPath)

        logger.info(f"ocr/qr start: pattern={item['pattern']}")
        result = ocr2qr.execOcr2Qr(outputPath, item["pattern"])
    except Exception as e:
        logger.error(f"process failed: {e}")
        logger.info(f"log: {LOG_FILE}")
        sys.exit(1)

    if not result:
        logger.warning("no match found")

    print("")
    print("Press any key to return to menu")
    funcReadKey()


def execShutdown():
    print("")
    print("Shutdown? Press 0 again to confirm")
    confirm = funcReadKey()
    if confirm == "0":
        logger.info("shutdown")
        subprocess.run(["sync"])
        # unmount usb drives before shutdown to prevent hang
        subprocess.run(["sudo", "umount", "-a", "-t", "vfat,exfat,ntfs"])
        subprocess.run(["sudo", "shutdown", "-h", "now"])


##########
# Startup check
##########

def execStartupCheck():
    if not os.path.isdir(SAVE_DIR):
        logger.error(f"save dir not found: {SAVE_DIR}")
        sys.exit(1)

    if not os.path.exists(f"/dev/video{VIDEO_DEVICE_INDEX}"):
        logger.error(f"capture device not found: /dev/video{VIDEO_DEVICE_INDEX}")
        sys.exit(1)

    if not os.path.isfile(MENU_JSON):
        logger.error(f"menu.json not found: {MENU_JSON}")
        sys.exit(1)

    if shutil.which("fbi") is None:
        logger.error("fbi not found or not in PATH -- sudo apt install fbi")
        sys.exit(1)


##########
# Main
##########

execStartupCheck()

menuItems = funcLoadMenu()
logger.info("menu started")
execShowMenu(menuItems)

buf = ""
while True:
    key = funcReadKey()
    buf += key

    # menu number
    matched = False
    for i, item in enumerate(menuItems, start=1):
        if buf == str(i):
            logger.info(f"select {i}")
            execRunCapture(item)
            execShowMenu(menuItems)
            buf = ""
            matched = True
            break

    if matched:
        continue

    # shutdown
    if buf == "0":
        execShutdown()
        execShowMenu(menuItems)
        buf = ""

    # exit
    elif buf == EXIT_SEQUENCE:
        logger.info("exit")
        sys.exit(0)

    # !shell! sequence
    elif buf == SHELL_SEQUENCE:
        logger.info("shell mode")
        subprocess.run(["/bin/bash"])
        execShowMenu(menuItems)

    # not a prefix of !shell! or !exit! -> clear buffer
    elif not SHELL_SEQUENCE.startswith(buf) and not EXIT_SEQUENCE.startswith(buf):
        buf = ""
