"""
Database model for Finly.

Uses SQLite (sqlite3). Provides CRUD operations for categories and transactions,
monthly summary calculations, and CSV export.

All dates are stored as ISO YYYY-MM-DD strings.

Creator: Maloth Harsha
"""
import csv
import os
import sqlite3
from datetime import datetime
from typing import List, Optional, Tuple


class Database:
    def __init__(self, db_path: Optional[str] = None):
        # Default DB location: data/expenses.db in package folder
        base = os.path.dirname(__file__)
        data_dir = os.path.join(base, "data")
        os.makedirs(data_dir, exist_ok=True)
        if db_path is None:
            db_path = os.path.join(data_dir, "expenses.db")

        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        cur = self.conn.cursor()
        # Enable foreign keys
        cur.execute("PRAGMA foreign_keys = ON;")

        # Categories table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
            """
        )

        # Transactions table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category_id INTEGER,
                type TEXT NOT NULL CHECK (type IN ('Income','Expense')),
                description TEXT,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
            )
            """
        )

        # Ensure there's at least a default category
        cur.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (1, 'Uncategorized')")

        self.conn.commit()

    # Category operations
    def get_categories(self) -> List[sqlite3.Row]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, name FROM categories ORDER BY name")
        return cur.fetchall()

    def add_category(self, name: str) -> int:
        cur = self.conn.cursor()
        cur.execute("INSERT INTO categories (name) VALUES (?)", (name.strip(),))
        self.conn.commit()
        return cur.lastrowid

    def update_category(self, category_id: int, name: str):
        cur = self.conn.cursor()
        cur.execute("UPDATE categories SET name = ? WHERE id = ?", (name.strip(), category_id))
        self.conn.commit()

    def delete_category(self, category_id: int) -> bool:
        # Prevent deleting default category with id 1
        if category_id == 1:
            return False
        cur = self.conn.cursor()
        # Check if any transactions reference this category
        cur.execute("SELECT COUNT(*) as cnt FROM transactions WHERE category_id = ?", (category_id,))
        if cur.fetchone()["cnt"] > 0:
            # Do not delete categories with associated transactions
            return False
        cur.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        self.conn.commit()
        return cur.rowcount > 0

    # Transaction operations
    def add_transaction(self, date: str, amount: float, category_id: Optional[int], t_type: str, description: Optional[str]) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO transactions (date, amount, category_id, type, description) VALUES (?, ?, ?, ?, ?)",
            (date, amount, category_id, t_type, description),
        )
        self.conn.commit()
        return cur.lastrowid

    def update_transaction(self, tx_id: int, date: str, amount: float, category_id: Optional[int], t_type: str, description: Optional[str]):
        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE transactions
            SET date = ?, amount = ?, category_id = ?, type = ?, description = ?
            WHERE id = ?
            """,
            (date, amount, category_id, t_type, description, tx_id),
        )
        self.conn.commit()

    def delete_transaction(self, tx_id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
        self.conn.commit()

    def get_transactions(self, year: Optional[int] = None, month: Optional[int] = None) -> List[sqlite3.Row]:
        cur = self.conn.cursor()
        if year and month:
            # Filter by month
            start = f"{year:04d}-{month:02d}-01"
            if month == 12:
                end = f"{year+1:04d}-01-01"
            else:
                end = f"{year:04d}-{month+1:02d}-01"
            cur.execute(
                """
                SELECT t.id, t.date, t.amount, t.type, t.description, c.id as category_id, c.name as category
                FROM transactions t
                LEFT JOIN categories c ON t.category_id = c.id
                WHERE date >= ? AND date < ?
                ORDER BY date DESC
                """,
                (start, end),
            )
        else:
            cur.execute(
                """
                SELECT t.id, t.date, t.amount, t.type, t.description, c.id as category_id, c.name as category
                FROM transactions t
                LEFT JOIN categories c ON t.category_id = c.id
                ORDER BY date DESC
                """
            )
        return cur.fetchall()

    def get_monthly_summary(self, year: int, month: int) -> Tuple[float, float, float]:
        cur = self.conn.cursor()
        start = f"{year:04d}-{month:02d}-01"
        if month == 12:
            end = f"{year+1:04d}-01-01"
        else:
            end = f"{year:04d}-{month+1:02d}-01"

        cur.execute(
            """
            SELECT type, SUM(amount) as total FROM transactions
            WHERE date >= ? AND date < ?
            GROUP BY type
            """,
            (start, end),
        )
        income = 0.0
        expense = 0.0
        for row in cur.fetchall():
            if row["type"] == "Income":
                income = row["total"] or 0.0
            else:
                expense = row["total"] or 0.0
        balance = (income or 0.0) - (expense or 0.0)
        return float(income), float(expense), float(balance)

    def export_csv(self, csv_path: str) -> None:
        rows = self.get_transactions()
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "date", "amount", "type", "category", "description"])
            for r in rows:
                writer.writerow([r["id"], r["date"], r["amount"], r["type"], r["category"], r["description"]])

    def close(self):
        self.conn.close()
