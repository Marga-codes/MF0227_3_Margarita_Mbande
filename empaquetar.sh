#!/usr/bin/env bash
# Genera el .zip de entrega a partir del último commit.
# git archive solo incluye archivos versionados, así que quedan fuera
# venv/, __pycache__/, db.sqlite3 y todo lo que ignora .gitignore.
set -euo pipefail
cd "$(dirname "$0")"
NOMBRE="MF0227_3_Margarita_Mbande"
git archive --format=zip --prefix="${NOMBRE}/" -o "${NOMBRE}.zip" HEAD
echo "Generado ${NOMBRE}.zip"
