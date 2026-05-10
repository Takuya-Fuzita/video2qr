# Changelog

## [1.0.0] - 2026-05-10

### Added
- HDMI frame capture via OpenCV (`hdmi2png.py`)
- OCR and regex extraction via Tesseract (`ocr2qr.py`)
- QR code generation with SHA-256 hash suffix for visual verification
- Full-screen QR display on framebuffer LCD via `fbi`
- Interactive menu driven by `menu.json` (no code changes needed to add patterns)
- Hidden commands: `!shell!` for maintenance shell, `!exit!` to quit
- Setup scripts for automated installation (`setup.sh` + `setup/`)
- English / Japanese language selection at setup
- udev rule to fix `/dev/dri/card0` and `card1` swap issue on Raspberry Pi 4
