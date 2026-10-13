# db1/mig_firm_acc.py

from db1.db import get_connection

MIGRATION_NAME = "firmAcc_1"

def migrate():
    with get_connection() as conn:
        try:
            conn.execute("BEGIN IMMEDIATE")

            # Ensure migration tracking exists
            conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    migration_name TEXT PRIMARY KEY,
                    applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Check whether this migration already ran
            existing = conn.execute(
                """
                SELECT 1
                FROM schema_migrations
                WHERE migration_name = ?
                """,
                (MIGRATION_NAME,)
            ).fetchone()

            if existing:
                print("Firm accounts migration already applied.")
                conn.rollback()
                return

            # Create firm accounts table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS firm_accounts (
                    firm_id INTEGER PRIMARY KEY,

                    balance INTEGER NOT NULL DEFAULT 0
                        CHECK (balance >= 0),

                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (firm_id)
                        REFERENCES firms(firm_id)
                        ON DELETE CASCADE
                )
            """)

            # Create accounts for all existing firms
            conn.execute("""
                INSERT OR IGNORE INTO firm_accounts (firm_id)
                SELECT firm_id
                FROM firms
            """)

            # Record completed migration
            conn.execute(
                """
                INSERT INTO schema_migrations (migration_name)
                VALUES (?)
                """,
                (MIGRATION_NAME,)
            )

            conn.commit()
            print("Firm accounts migration complete.")

        except Exception:
            conn.rollback()
            raise


if __name__ == "__main__":
    migrate()