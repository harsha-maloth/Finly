
# Finly — Minimal, private finance tracking.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) ![Desktop App](https://img.shields.io/badge/Platform-Desktop-lightgrey) ![Offline](https://img.shields.io/badge/Offline-Only-green) ![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)

Finly is a tiny, privacy-first personal finance tracker that runs entirely on your computer. It stores all data locally in a SQLite database and requires no network access, accounts, or telemetry.

Key features
- Add, edit, and delete income and expense transactions
- User-defined categories (create/edit/delete)
- Monthly summaries (total income, total expenses, balance)
- Export all transactions to CSV
- Local SQLite backend (no cloud, no tracking)

About Finly

Mission
: Finly provides a simple, transparent, and fully offline way to track personal income and expenses while giving users complete ownership of their financial data.

Core values: Privacy-first, simplicity, ownership, transparency, reliability

Installation

1. Create and activate a Python virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install runtime dependencies:

```bash
pip install -r expense_tracker/requirements.txt
```

Run

```bash
python -m expense_tracker.main
```

Where data is stored

Finly stores its data locally in a SQLite database created at:

```
expense_tracker/data/expenses.db
```

This file is purely local. Back it up if you need to move your data.

Disclaimer

Finly is provided for personal bookkeeping and learning purposes and is not financial advice. Use at your own discretion.

Author

Creator: Maloth Harsha

GitHub: https://github.com/harsha-maloth

Contributing

See `CONTRIBUTING.md` for a beginner-friendly guide to contribute. Finly is intentionally small and local-only; please respect the offline-first philosophy when proposing changes.

