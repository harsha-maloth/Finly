#!/usr/bin/env bash
set -euo pipefail

# Build Finly with PyInstaller (one-folder build).
# Run this from the repository root with virtualenv activated.

APP_NAME=finly
ENTRY=expense_tracker/main.py
DIST_DIR=dist/${APP_NAME}

echo "Cleaning previous builds..."
rm -rf build/ dist/ ${APP_NAME}.spec || true

echo "Running PyInstaller..."
pyinstaller --noconfirm --windowed --name ${APP_NAME} \
  --add-data "expense_tracker/data${PATHSEP:-:}expense_tracker/data" \
  ${ENTRY}

echo "One-folder build available at: ${DIST_DIR}"

echo "Done. Use packaging/create_deb.sh or create_rpm.sh to make native packages, or create_appimage.sh for AppImage."
