#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
FONT_DIR="$SCRIPT_DIR/fonts"
LICENSE_DIR="$FONT_DIR/licenses"

mkdir -p "$FONT_DIR" "$LICENSE_DIR"

download() {
  local destination="$1"
  local url="$2"

  if [ -s "$destination" ]; then
    return
  fi

  printf 'Загрузка %s...\n' "$(basename "$destination")"
  curl -L --fail --retry 3 --connect-timeout 15 -o "$destination" "$url"
}

download "$FONT_DIR/01-BadScript-Regular.ttf" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/badscript/BadScript-Regular.ttf"
download "$FONT_DIR/02-Caveat-Regular.ttf" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/caveat/Caveat%5Bwght%5D.ttf"
download "$FONT_DIR/03-MarckScript-Regular.ttf" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/marckscript/MarckScript-Regular.ttf"
download "$FONT_DIR/04-Neucha-Regular.ttf" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/neucha/Neucha.ttf"
download "$FONT_DIR/05-Pacifico-Regular.ttf" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/pacifico/Pacifico-Regular.ttf"
download "$FONT_DIR/06-Lobster-Regular.ttf" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/lobster/Lobster-Regular.ttf"
download "$FONT_DIR/07-AmaticSC-Regular.ttf" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/amaticsc/AmaticSC-Regular.ttf"
download "$FONT_DIR/08-Pangolin-Regular.ttf" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/pangolin/Pangolin-Regular.ttf"
download "$FONT_DIR/09-SwankyAndMooMoo-Regular.ttf" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/swankyandmoomoo/SwankyandMooMoo.ttf"
download "$FONT_DIR/10-KellySlab-Regular.ttf" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/kellyslab/KellySlab-Regular.ttf"

download "$LICENSE_DIR/OFL-BadScript.txt" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/badscript/OFL.txt"
download "$LICENSE_DIR/OFL-Caveat.txt" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/caveat/OFL.txt"
download "$LICENSE_DIR/OFL-MarckScript.txt" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/marckscript/OFL.txt"
download "$LICENSE_DIR/OFL-Neucha.txt" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/neucha/OFL.txt"
download "$LICENSE_DIR/OFL-Pacifico.txt" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/pacifico/OFL.txt"
download "$LICENSE_DIR/OFL-Lobster.txt" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/lobster/OFL.txt"
download "$LICENSE_DIR/OFL-AmaticSC.txt" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/amaticsc/OFL.txt"
download "$LICENSE_DIR/OFL-Pangolin.txt" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/pangolin/OFL.txt"
download "$LICENSE_DIR/OFL-SwankyAndMooMoo.txt" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/swankyandmoomoo/OFL.txt"
download "$LICENSE_DIR/OFL-KellySlab.txt" \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/kellyslab/OFL.txt"

printf '%s\n' "Бесплатные рукописные шрифты установлены."
