# Finly — Minimal, private finance tracking.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) ![Desktop App](https://img.shields.io/badge/Platform-Desktop-lightgrey) ![Offline](https://img.shields.io/badge/Offline-Only-green) ![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)

Finly is a small, privacy-first personal finance tracker that runs entirely on your computer. It stores all data locally in a SQLite database and requires no network access, accounts, or telemetry.

Features
- Add, edit, and delete income and expense transactions
- User-defined categories (create/edit/delete)
- Monthly summaries (total income, total expenses, balance)
- Export all transactions to CSV
- Local SQLite backend (no cloud, no tracking)


Installation

Choose the installer for your distribution and install it. Download the `.deb` for Debian/Ubuntu or the `.rpm` for Fedora/openSUSE.

Debian/Ubuntu:

```bash
sudo dpkg -i finly_0.1.0_amd64.deb
# or use apt to fix deps: sudo apt-get install -f
```

Fedora/openSUSE:

```bash
sudo rpm -Uvh finly-0.1.0-1.x86_64.rpm
# or use dnf: sudo dnf install ./finly-0.1.0-1.x86_64.rpm
```

After installation you should find Finly in your desktop environment (Applications menu). You can also run the shipped executable directly:

```bash
/opt/finly/finly
```

Data storage and backups

Finly stores data locally in a SQLite database under your user data directory (for packaged installs the app copies a starter DB to your XDG data location, commonly `~/.local/share/finly/expenses.db`). Back up that file if you want to keep or migrate your data.

If you prefer to run from source (developer mode), see the `expense_tracker` directory. Running from source will also create or use a local `expense_tracker/data/expenses.db`.

Disclaimer

Finly is not financial advice. It is a simple tool for tracking personal finances and a learning project for the author.

Author

Creator: Maloth Harsha

GitHub: https://github.com/harsha-maloth
