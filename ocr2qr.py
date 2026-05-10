import os
import re
import hashlib
import logging
import subprocess

import cv2
import numpy as np
import pytesseract
import qrcode

logger = logging.getLogger("ocr2qr")

#########
# Constants
#########

SAVE_DIR = "/var/opt/pics"

QR_MAX_LEN = 128 # longer strings make QR too dense. fine if LCD is large
QR_SIZE    = 280
CANVAS_W = 320
CANVAS_H = 480


###########
# Helper funcs
###########

def funcGenHash5(text):
    # hash input with SHA-256 and return last 5 hex chars
    # (collision chance is about 1-in-a-million with 5 hex chars)
    digest = hashlib.sha256(text.encode()).hexdigest()
    return digest[-5:]


def funcBuildQrImage(matched, hash5):
    # generate QR
    qr = qrcode.QRCode(border=2)
    qr.add_data(matched)
    qr.make(fit=True)
    qrImg = qr.make_image(fill_color="black", back_color="white")
    qrImg = np.array(qrImg.convert("RGB"))
    qrImg = cv2.cvtColor(qrImg, cv2.COLOR_RGB2BGR)

    # resize QR to fixed size
    qrImg = cv2.resize(qrImg, (QR_SIZE, QR_SIZE), interpolation=cv2.INTER_NEAREST)

    # create white canvas
    canvas = np.ones((CANVAS_H, CANVAS_W, 3), dtype=np.uint8) * 255

    # paste QR to top-center of canvas
    xOffset = (CANVAS_W - QR_SIZE) // 2
    canvas[:QR_SIZE, xOffset:xOffset + QR_SIZE] = qrImg

    # draw hash suffix
    cv2.putText(canvas, hash5,
        (CANVAS_W // 2 - 40, QR_SIZE + 30),
        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0, 0),2)

    # draw original string (wrap every 20 chars)
    lineW = 20
    lines = [matched[i:i + lineW] for i in range(0, len(matched), lineW)]
    y = QR_SIZE + 55
    for line in lines:
        cv2.putText(canvas, line,
            (10, y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (80,80,80),1)
        y += 18

    return canvas

########
# Main
########

def execOcr2Qr(imagePath, pattern):
    # load image
    img = cv2.imread(imagePath)
    if img is None:
        logger.error(f"cannot load image: {imagePath}")
        raise RuntimeError(f"cannot load image: {imagePath}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # upscale
    src  = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    # OCR with alphanumeric whitelist
    config = r"--psm 6 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = pytesseract.image_to_string(src, config=config)
    
    logger.debug(f"ocr result: {repr(text)}")

    # regex match
    match = re.search(pattern, text)
    if not match:
        logger.info(f"no match: pattern={pattern}")
        return False

    matched = match.group(0)

    # length check
    if len(matched) > QR_MAX_LEN:
        logger.error(f"too long: {len(matched)} chars (limit={QR_MAX_LEN})")
        raise RuntimeError(f"too long: {len(matched)} chars (limit={QR_MAX_LEN})")

    logger.info(f"match: {matched}")

    # generate hash  
    hash5 = funcGenHash5(matched)
    logger.info(f"hash5: {hash5}")

    # build and save QR+text image
    base = os.path.splitext(os.path.basename(imagePath))[0]
    qrPath = os.path.join(SAVE_DIR, f"{base}_qr.png")
    outImg = funcBuildQrImage(matched, hash5)
    cv2.imwrite(qrPath, outImg)
    logger.info(f"qr saved: {qrPath}")

    # display fullscreen with fbi
    subprocess.run(["fbi", "-d", "/dev/dri/hdmi-card", "-T", "1", "-noverbose", "-a", qrPath])
    return True
