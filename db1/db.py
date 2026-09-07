#db.py
import sqlite3, random
from pathlib import Path

DB_PATH = Path("storage/data/ardent.db")
SCHEMA_PATH = Path("storage/data/schema.sql")

print(f"Using database: {DB_PATH.resolve()}")
# Debug & eval

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

def get_balance(user_id: int) -> int:
    user = get_or_create_user(user_id)
    return user["balance"]

def get_wage(user_id: int) -> int:
    user = get_or_create_user(user_id)
    return user["wage"]

def work_user(user_id: int):
    with get_connection() as connection:
        connection.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,),
        )

        connection.execute(
            """
            UPDATE users
            SET balance = balance + wage,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            (user_id,),
        )

        return connection.execute(
            """
            SELECT balance, wage
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

# I dont remember coding, I just black out and let the spirit of python take over me

def transfer_balance(sender_id: int, recipient_id: int, amount: int):
    if amount <= 0:
        raise ValueError("Please enter a positive value to transfer.")

    with get_connection() as connection:
        connection.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (sender_id,),
        )
        connection.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (recipient_id,),
        )

        sender = connection.execute(
            "SELECT balance FROM users WHERE user_id = ?",
            (sender_id,),
        ).fetchone()

        if sender["balance"] < amount:
            raise ValueError("Insufficient balance.")

        connection.execute(
            """
            UPDATE users
            SET balance = balance - ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            (amount, sender_id),
        )

        connection.execute(
            """
            UPDATE users
            SET balance = balance + ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            (amount, recipient_id),
        )

        connection.execute(
            """
            INSERT INTO transactions (
                sender_id,
                recipient_id,
                amount,
                transaction_type
            )
            VALUES (?, ?, ?, ?)
            """,
            (sender_id, recipient_id, amount, "transfer"),
        )

# Add gamba:
def coin_flip(user_id: int, guess: str, wager: int):
    guess = guess.lower()

    if guess not in ("heads", "tails"):
        raise ValueError("Guess must be heads or tails.")

    if wager <= 0:
        raise ValueError("Wager must be greater than zero.")

    with get_connection() as connection:
        connection.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,),
        )

        user = connection.execute(
            """
            SELECT balance FROM users WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

        if user["balance"] < wager:
            raise ValueError("Insufficient balance.")

        result = random.choice(["heads", "tails"])

        if result == guess:
            connection.execute(
                """
                UPDATE users
                SET balance = balance + ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
                """,
                (wager, user_id),
            )
            connection.execute(
                """
                INSERT INTO transactions (recipient_id,
                                          amount,
                                          transaction_type)
                VALUES (?, ?, 'coin_win')
                """,
                (user_id, wager),
            )

            won = True
        else:
            connection.execute(
                """
                UPDATE users
                SET balance = balance - ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
                """,
                (wager, user_id),
            )
            connection.execute(
                """
                INSERT INTO transactions (sender_id,
                                          amount,
                                          transaction_type)
                VALUES (?, ?, 'coin_loss')
                """,
                (user_id, wager),
            )

            won = False

        new_balance = connection.execute(
            "SELECT balance FROM users WHERE user_id = ?",
            (user_id,),
        ).fetchone()["balance"]

        return result, won, new_balance