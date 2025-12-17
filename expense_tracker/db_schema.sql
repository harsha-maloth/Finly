-- SQLite schema for Finly
-- Creator: Maloth Harsha

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    category_id INTEGER,
    type TEXT NOT NULL CHECK (type IN ('Income','Expense')),
    description TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- Insert default category
INSERT OR IGNORE INTO categories (id, name) VALUES (1, 'Uncategorized');
