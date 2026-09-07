import sqlite3
from pathlib import Path

DB_PATH = Path("storage/data/ardent.db1")
SCHEMA_PATH = Path("storage/data/schema.sql")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as connection:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            connection.executescript(schema_file.read())


def get_or_create_user(user_id: int):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO users (user_id)
            VALUES (?)
            """,
            (user_id,),
        )

        return connection.execute(
            """
            SELECT *
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()