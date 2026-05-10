import cv2
import logging

logger = logging.getLogger("capture")

DEVICE_INDEX = 0


def execCapture(outputPath):
    cap = cv2.VideoCapture(DEVICE_INDEX)
    if not cap.isOpened():
        logger.error(f"cannot open device {DEVICE_INDEX}")
        raise RuntimeError(f"cannot open device {DEVICE_INDEX}")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

    # discard a few frames
    for _ in range(5):
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if not ret:
        logger.error("failed to grab frame")
        raise RuntimeError("failed to grab frame")

    cv2.imwrite(outputPath, frame)
    logger.info(f"saved:{outputPath}")
