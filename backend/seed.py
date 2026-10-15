"""Load seed_data.sql into content_mod.db, only if the posts table is empty."""
import sqlite3

conn = sqlite3.connect("content_mod.db")
if conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0] == 0:
    with open("seed_data.sql", encoding="utf-8") as f:
        conn.executescript(f.read())
    print("Seed data loaded.")
else:
    print("Posts table not empty, skipping seed data.")
conn.close()
