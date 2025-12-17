Quick packaging commands (copy-paste)

Linux (build, then make deb/rpm/AppImage):

```bash
# 1) build pyinstaller one-folder
./packaging/build_pyinstaller.sh

# 2a) create deb (requires fpm)
./packaging/create_deb.sh

# 2b) create rpm (requires fpm)
./packaging/create_rpm.sh

# 2c) AppImage (requires appimagetool)
./packaging/create_appimage.sh
```

Windows (recommended on Windows host)

```powershell
# install pyinstaller in your venv and run on Windows
pyinstaller --noconfirm --windowed --name finly expense_tracker/main.py
# then use the NSIS script with makensis
makensis packaging\windows\finly_nsis.nsi
```

Notes
- Tools such as `fpm`, `appimagetool`, and `makensis` are required to produce the final packages. Install them through your platform package manager.
- The one-folder PyInstaller build is easiest to inspect and package. Use `--onefile` only if you explicitly want a single binary.
