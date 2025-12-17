# Finly — Minimal, private finance tracking.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) ![Desktop App](https://img.shields.io/badge/Platform-Desktop-lightgrey) ![Offline](https://img.shields.io/badge/Offline-Only-green) ![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)

Finly is a small, privacy-first personal finance tracker that runs entirely on your computer. It stores all data locally in a SQLite database and requires no network access, accounts, or telemetry.

Features
- Add, edit, and delete income and expense transactions
- User-defined categories (create/edit/delete)
- Monthly summaries (total income, total expenses, balance)
- Export all transactions to CSV
- Local SQLite backend (no cloud, no tracking)

Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r expense_tracker/requirements.txt
python -m expense_tracker.main
```

Data storage

Finly stores data in `expense_tracker/data/expenses.db`. This file is local; back it up manually if you want to transfer your data.

Disclaimer

Finly is not financial advice. It is a simple tool for tracking personal finances and a learning project for the author.

Author

Creator: Maloth Harsha

GitHub: https://github.com/harsha-maloth
