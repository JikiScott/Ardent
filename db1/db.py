#db.py
import sqlite3, random
from pathlib import Path
from decimal import Decimal
from econ.crystals import get_crystal_equivalency

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
# CRYSTALS

VALID_CRYSTAL_OWNER_TYPES = {
    "user",
    "firm",
    "treasury",
}

def normalize_crystal(
    crystal_class: str,
    grade: str
) -> tuple[str, str]:
    crystal_class = crystal_class.lower()
    grade = grade.lower()

    # Raise ValueError if this combo no exist.
    get_crystal_equivalency(crystal_class, grade)
    return crystal_class, grade


def normalize_owner_type(owner_type: str) -> str:
    owner_type = owner_type.lower()

    if owner_type not in VALID_CRYSTAL_OWNER_TYPES:
        raise ValueError(
            f"Invalid owner type: {owner_type}"
        )

    return owner_type


def get_crystal_balance(
    owner_type: str,
    owner_id: int,
    crystal_class: str,
    grade: str
) -> Decimal:

    owner_type = normalize_owner_type(owner_type)
    crystal_class, grade = normalize_crystal(
        crystal_class,
        grade
    )

    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT quantity
            FROM crystal_inventory
            WHERE owner_type = ?
              AND owner_id = ?
              AND crystal_class = ?
              AND grade = ?
            """,
            (
                owner_type,
                owner_id,
                crystal_class,
                grade
            )
        ).fetchone()

    if row is None:
        return Decimal("0")

    return Decimal(row["quantity"])

def add_crystals(
    owner_type: str,
    owner_id: int,
    crystal_class: str,
    grade: str,
    quantity: Decimal
) -> Decimal:
    if quantity <= 0:
        raise ValueError("Crystal quantity must be positive.")

    owner_type = normalize_owner_type(owner_type)
    crystal_class, grade = normalize_crystal(
        crystal_class,
        grade
    )

    with get_connection() as conn:
        current = conn.execute(
            """
            SELECT quantity
            FROM crystal_inventory
            WHERE owner_type = ?
              AND owner_id = ?
              AND crystal_class = ?
              AND grade = ?
            """,
            (owner_type, owner_id, crystal_class, grade)
        ).fetchone()

        old_quantity = (
            Decimal(current["quantity"])
            if current is not None
            else Decimal("0")
        )

        new_quantity = old_quantity + quantity

        conn.execute(
            """
            INSERT INTO crystal_inventory
                (owner_type, owner_id, crystal_class, grade, quantity)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(owner_type, owner_id, crystal_class, grade)
            DO UPDATE SET quantity = excluded.quantity
            """,
            (
                owner_type,
                owner_id,
                crystal_class,
                grade,
                str(new_quantity)
            )
        )

        conn.commit()

    return new_quantity

def validate_firm_name(name: str) -> str:
    name = name.strip()

    if len(name) < 3:
        raise ValueError(
            "Firm names must be at least 3 characters long."
        )

    if len(name) > 50:
        raise ValueError(
            "Firm names cannot exceed 50 characters."
        )

    if not any(char.isalnum() for char in name):
        raise ValueError(
            "Firm names must contain at least one letter or number."
        )

    if any(char in "\r\n\t" for char in name):
        raise ValueError(
            "Firm names cannot contain line breaks or tabs."
        )


    if "@everyone" in name.lower() or "@here" in name.lower():
        raise ValueError(
            "Firm names cannot contain mass mentions."
        )

    if "<@" in name or "<#" in name:
        raise ValueError(
            "Firm names cannot contain Discord mentions."
        )

    if any(char in "!?,;@#" for char in name):
        raise ValueError(
            "Firm names cannot contain special characters."
        )

    return name

def create_firm(owner_id: int, name: str):

    name = validate_firm_name(name)
    #From above
    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO users (user_id)
                VALUES (?)
                """,
                (owner_id,)
            )

            cursor = conn.execute(
                """
                INSERT INTO firms (name, owner_id)
                VALUES (?, ?)
                """,
                (name, owner_id)
            )

            firm_id = cursor.lastrowid

            conn.execute(
                """
                INSERT INTO firm_members (firm_id, user_id, role)
                VALUES (?, ?, ?)
                """,
                (firm_id, owner_id, "owner")
            )

            return firm_id
    except sqlite3.IntegrityError as error:
        if "firms.name" in str(error):
            raise ValueError(
                "A firm with that name already exists!"
            ) from error

        if "firm_members.user_id" in str(error):
            raise ValueError(
                "You are already employed by a firm."
            ) from error

        raise


def get_user_firm(user_id: int):
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT
                firms.firm_id,
                firms.name,
                firms.owner_id,
                firm_members.role
            FROM firm_members
            JOIN firms
                ON firms.firm_id = firm_members.firm_id
            WHERE firm_members.user_id = ?
            """,
            (user_id,)
        ).fetchone()

def add_firm_member(
    firm_id: int,
    user_id: int,
    role: str = "laborer"
):
    with get_connection() as conn:
        # Check user exists
        conn.execute(
            """
            INSERT OR IGNORE INTO users (user_id)
            VALUES (?)
            """,
            (user_id,)
        )

        conn.execute(
            """
            INSERT INTO firm_members (firm_id, user_id, role)
            VALUES (?, ?, ?)
            """,
            (firm_id, user_id, role)
        )