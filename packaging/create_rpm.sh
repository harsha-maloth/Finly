#!/usr/bin/env bash
set -euo pipefail

# Create an RPM package for Finly using fpm.
# Requires: fpm

APP_NAME=finly
VERSION=0.1.0
DIST_DIR=dist/${APP_NAME}
PKG_DIR=package_root_rpm

if [ ! -d "${DIST_DIR}" ]; then
  echo "Error: ${DIST_DIR} not found. Run packaging/build_pyinstaller.sh first." >&2
  exit 2
fi

rm -rf ${PKG_DIR}
mkdir -p ${PKG_DIR}/opt/${APP_NAME}
cp -r ${DIST_DIR}/* ${PKG_DIR}/opt/${APP_NAME}/

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

echo "Building .rpm with fpm..."
fpm -s dir -t rpm -n ${APP_NAME} -v ${VERSION} --prefix=/ -C ${PKG_DIR} .

echo "Done. .rpm created in current directory."
