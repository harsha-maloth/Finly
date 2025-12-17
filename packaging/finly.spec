# PyInstaller spec file for Finly. Generated as example; pyinstaller can also be called
# directly via the CLI. Place this file in repository root or packaging/ and run:
# pyinstaller finly.spec

block_cipher = None

a = Analysis(
    ['expense_tracker/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[('expense_tracker/data', 'expense_tracker/data')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts, [], name='finly', debug=False, bootloader_ignore_signals=False, strip=False, upx=True, console=False)
