#!/bin/bash

set -euo pipefail
cd "$(dirname "$0")"

printf '%s\n' "Сборка Handwriting Print Studio.app"

if [ "$(uname -s)" != "Darwin" ]; then
  printf '%s\n' "Сборка .app выполняется только на macOS."
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' "Python 3 не найден."
  exit 1
fi

bash scripts/install_free_fonts.sh

if [ ! -d ".build-venv" ]; then
  python3 -m venv .build-venv
fi

source .build-venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt "pyinstaller>=6.10,<7"

python3 -m PyInstaller --noconfirm --clean HandwritingPrintStudio.spec

APP_PATH="dist/Handwriting Print Studio.app"
ZIP_PATH="dist/Handwriting-Print-Studio-macOS-arm64-v0.2.1.zip"

codesign --force --deep --sign - "$APP_PATH"
ditto -c -k --sequesterRsrc --keepParent "$APP_PATH" "$ZIP_PATH"

printf '\n%s\n' "Сборка завершена:"
printf '%s\n' "$APP_PATH"
printf '%s\n' "$ZIP_PATH"
open dist
