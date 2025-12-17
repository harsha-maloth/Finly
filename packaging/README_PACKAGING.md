Finly Packaging Guide
=====================

This folder contains helper scripts and configuration snippets to build desktop installers and packages for Finly. The repository contains the full source; these scripts prepare a distributable build using PyInstaller and common packaging tools.

Important
---------
- These scripts do NOT modify application logic. They build a local-only, offline desktop app based on the current source.
- Building Windows `.exe` installers must be performed on Windows or a compatible cross-build environment. Building native macOS `.dmg` requires macOS. Linux packaging is easiest from a Linux host.
- APK (Android) is not supported for PySide6-based desktop apps in any straightforward, reliable way. See "Android note" below.

Prerequisites (examples)
------------------------
- Python 3.8+
- Virtual environment with project deps installed (PySide6).
- PyInstaller
- fpm (for creating .deb and .rpm) — https://github.com/jordansissel/fpm (requires Ruby)
- appimagetool or linuxdeploy for AppImage
- nsis/makensis for Windows installer (if on Windows)

Quick build flow (Linux) — produce a one-folder executable
---------------------------------------------------------
1. Create and activate venv and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r expense_tracker/requirements.txt pyinstaller
```

2. Build with PyInstaller (one-folder recommended for packaging):

```bash
./packaging/build_pyinstaller.sh
# or directly:
pyinstaller --noconfirm --windowed --name finly --add-data "expense_tracker/data:expense_tracker/data" expense_tracker/main.py
```

3. After this, a `dist/finly/` folder will contain the runnable app. Use packaging scripts below to wrap it into a .deb, .rpm, AppImage or Windows installer.

Packaging scripts in this folder
-------------------------------
- `build_pyinstaller.sh` - Runs PyInstaller to create a one-folder build under `dist/finly/`.
- `create_deb.sh` - Packages the one-folder build into a Debian `.deb` using `fpm`.
- `create_rpm.sh` - Packages into an RPM using `fpm`.
- `create_appimage.sh` - Assembles an AppDir and uses AppImage tools to make an AppImage.
- `windows/finly_nsis.nsi` - Example NSIS script that can be used on Windows to create an installer from a PyInstaller one-folder build.
- `finly.spec` - Example PyInstaller spec file for custom builds (optional).

Android (APK) note
-------------------
PySide6 desktop applications are not designed for Android packaging with standard Python packaging tools. Building a native Android APK from this code would require porting the UI to a mobile-friendly toolkit (for example Kivy or using Qt for Android with a Qt build process) and is out of scope for these scripts. If you want an Android app, consider one of:

- Rewriting the UI with Kivy and using Buildozer / Briefcase to create an APK.
- Using Qt for Android (complex: requires building Qt for Android, creating Android project and integrating Python via a bridge). Not recommended for beginners.

Support
-------
If any of the commands here fail, copy the terminal output and I can help adjust the script or fix missing steps.
