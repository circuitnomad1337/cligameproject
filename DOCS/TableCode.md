# USERS TABLE

    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        level INT DEFAULT 1,
        coins INT DEFAULT 0,
        gems INT DEFAULT 0,
        platinum INT DEFAULT 0,
        fountain_claimed BOOL DEFAULT False,
        title TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );


# TBD...