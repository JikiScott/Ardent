PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER NOT NULL DEFAULT 0,
    wage INTEGER NOT NULL DEFAULT 1,
    job_level INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    recipient_id INTEGER,
    amount INTEGER NOT NULL CHECK (amount > 0),
    transaction_type TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (recipient_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS crystal_inventory (
    owner_type TEXT NOT NULL,
    owner_id INTEGER NOT NULL,
    crystal_class TEXT NOT NULL,
    grade TEXT NOT NULL,
    quantity TEXT NOT NULL DEFAULT '0',

    PRIMARY KEY (owner_type, owner_id, crystal_class, grade)
);

CREATE TABLE IF NOT EXISTS firms (
    firm_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    owner_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS firm_members (
    firm_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL UNIQUE,
    role TEXT NOT NULL DEFAULT 'laborer',
    joined_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (firm_id, user_id),

    FOREIGN KEY (firm_id) REFERENCES firms(firm_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- EMPLOY INVITES
CREATE TABLE IF NOT EXISTS firm_invites (
    firm_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    invited_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (firm_id, user_id),

    FOREIGN KEY (firm_id)
        REFERENCES firms(firm_id)
        ON DELETE CASCADE,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

-- TREASURY
CREATE TABLE IF NOT EXISTS treasury (
    treasury_id INTEGER PRIMARY KEY CHECK (treasury_id = 1),

    balance INTEGER NOT NULL DEFAULT 0
        CHECK (balance >= 0),

    daily_issuance_limit INTEGER NOT NULL DEFAULT 9600
        CHECK (daily_issuance_limit >= 0),

    issued_today INTEGER NOT NULL DEFAULT 0
        CHECK (issued_today >= 0),

    total_issued INTEGER NOT NULL DEFAULT 0
        CHECK (total_issued >= 0),

    last_issuance_date TEXT,

    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT OR IGNORE INTO treasury (
    treasury_id,
    balance,
    daily_issuance_limit
)
VALUES (
    1,
    9600,
    9600
);
CREATE TABLE IF NOT EXISTS treasury_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    amount INTEGER NOT NULL CHECK (amount > 0),

    transaction_type TEXT NOT NULL,

    user_id INTEGER,
    firm_id INTEGER,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    FOREIGN KEY (firm_id)
        REFERENCES firms(firm_id)
        ON DELETE SET NULL
);