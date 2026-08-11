import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Users Table
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT,
role TEXT
)
""")

# Complaints Table
cur.execute("""
CREATE TABLE IF NOT EXISTS complaints(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
subject TEXT,
message TEXT,
status TEXT
)
""")

# Default Admin
cur.execute("""
INSERT OR IGNORE INTO users
VALUES (1,'Admin','admin@gmail.com','admin123','admin')
""")

conn.commit()
conn.close()

print("Database Created Successfully")
