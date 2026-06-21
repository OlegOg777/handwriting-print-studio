#!/bin/bash

set -e
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  osascript -e 'display alert "Не найден Python 3" message "Установите Python 3 и запустите файл снова."'
  exit 1
fi

bash scripts/install_free_fonts.sh

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
