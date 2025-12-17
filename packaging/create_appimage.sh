#!/usr/bin/env bash
set -euo pipefail

# Create an AppImage for Finly
# Requires: linuxdeploy (or appimagetool). This script produces an AppDir and calls appimagetool if available.

APP_NAME=finly
DIST_DIR=dist/${APP_NAME}
APPDIR=${APP_NAME}.AppDir

if [ ! -d "${DIST_DIR}" ]; then
  echo "Error: ${DIST_DIR} not found. Run packaging/build_pyinstaller.sh first." >&2
  exit 2
fi

rm -rf ${APPDIR}
mkdir -p ${APPDIR}/usr/bin
cp -r ${DIST_DIR}/* ${APPDIR}/usr/bin/

mkdir -p ${APPDIR}/usr/share/applications
cat > ${APPDIR}/usr/share/applications/${APP_NAME}.desktop <<'EOF'
[Desktop Entry]
Name=Finly
Comment=Minimal, private finance tracking
Exec=finly
Icon=finly
Terminal=false
Type=Application
Categories=Utility;Finance;
EOF

mkdir -p ${APPDIR}/usr/share/icons/hicolor/256x256/apps
echo "(Place a finly 256x256 PNG icon at ${APPDIR}/usr/share/icons/hicolor/256x256/apps/finly.png)"

if command -v appimagetool >/dev/null 2>&1; then
  echo "Running appimagetool to create AppImage..."
  appimagetool ${APPDIR}
  echo "AppImage created."
else
  echo "appimagetool not found. ${APPDIR} prepared; package it manually or install appimagetool to create an AppImage."
fi
