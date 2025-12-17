#!/usr/bin/env bash
set -euo pipefail

# Create a Debian package for Finly from a PyInstaller one-folder build.
# Requires: fpm (https://github.com/jordansissel/fpm)
# Usage: build with build_pyinstaller.sh first, then run this script.

APP_NAME=finly
VERSION=0.1.0
DIST_DIR=dist/${APP_NAME}
PKG_DIR=package_root

if [ ! -d "${DIST_DIR}" ]; then
  echo "Error: ${DIST_DIR} not found. Run packaging/build_pyinstaller.sh first." >&2
  exit 2
fi

echo "Preparing package layout..."
rm -rf ${PKG_DIR}
mkdir -p ${PKG_DIR}/opt/${APP_NAME}
cp -r ${DIST_DIR}/* ${PKG_DIR}/opt/${APP_NAME}/

# Add a .desktop file for Linux desktop integration
mkdir -p ${PKG_DIR}/usr/share/applications
cat > ${PKG_DIR}/usr/share/applications/${APP_NAME}.desktop <<'EOF'
[Desktop Entry]
Name=Finly
Comment=Minimal, private finance tracking
Exec=/opt/finly/finly
Icon=finly
Terminal=false
Type=Application
Categories=Utility;Finance;
EOF

echo "Building .deb with fpm..."
fpm -s dir -t deb -n ${APP_NAME} -v ${VERSION} --prefix=/ \
  -C ${PKG_DIR} .

echo "Done. .deb created in current directory."
