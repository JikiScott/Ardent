import sqlite3
from db1.db import DB_PATH
from econ.currency import FARTHINGS_PER_POUND

MIGRATION_NAME = "sov2farth1"

def migrate_currency():
    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("BEGIN IMMEDIATE")

        connection.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                migration_name TEXT PRIMARY KEY,
                applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        existing = connection.execute("""
            SELECT 1
            FROM schema_migrations
            WHERE migration_name = ?
        """, (MIGRATION_NAME,)).fetchone()

        if existing:
            print("Currency migration already done.")
            connection.rollback()
            return

        connection.execute("""
            UPDATE users
            SET balance = balance * ?,
                wage = wage * ?,
                updated_at = CURRENT_TIMESTAMP
        """, (
            FARTHINGS_PER_POUND,
            FARTHINGS_PER_POUND
        ))

        connection.execute("""
            UPDATE transactions
            SET amount = amount * ?
        """, (FARTHINGS_PER_POUND,))

        connection.execute("""
            INSERT INTO schema_migrations (migration_name)
            VALUES (?)
        """, (MIGRATION_NAME,))

        connection.commit()
        print("Currency migration complete 🔥.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    migrate_currency()