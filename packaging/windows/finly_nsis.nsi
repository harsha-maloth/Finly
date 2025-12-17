; NSIS installer script for Finly (example)
; Build on Windows with NSIS installed (makensis)

!define APPNAME "Finly"
!define VERSION "0.1.0"
!define OUTFILE "Finly-Installer-${VERSION}.exe"
!define INSTALLDIR "$PROGRAMFILES\\Finly"

Name "${APPNAME} ${VERSION}"
OutFile "${OUTFILE}"
InstallDir "${INSTALLDIR}"

Section "Install"
  SetOutPath "$INSTDIR"
  ; Copy all files from the PyInstaller one-folder build (place files next to this script or adjust path)
  File /r "dist\\finly\\*"
  ; Create shortcut
  CreateShortCut "$DESKTOP\\Finly.lnk" "$INSTDIR\\finly.exe"
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\\Finly.lnk"
  RMDir /r "$INSTDIR"
SectionEnd
