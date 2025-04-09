from flask import Flask, request, jsonify
import psycopg2
import hashlib

"""
PLACEHOLDER FOR TABLE'S DATA CREATION

                        CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    level INT DEFAULT 1,
                    coins INT DEFAULT 0,
                    gems INT default 0,
                    platinum INT DEFAULT 0
                    fountain_claimed BOOL
                    title TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );


"""

CONNECTION = psycopg2.connect(
    dbname = "game_db",
    user = "game_db_user",
    password = "",
    host = "0.0.0.0",
    port = 5432
)

CURSOR = CONNECTION.cursor()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class User:
    @staticmethod
    def login(username, password):
        try:
            CURSOR.execute("SELECT password_hash FROM users where USERNAME = %s", (username,))
            result = CURSOR.fetchone()

            if not result or hash_password(password) != result[0]:
                return False

            return True

        except Exception as e:
            print(f"Error during login: {e}.")
            return False

    @staticmethod
    def register(username, password):
        try:
            CURSOR.execute("SELECT 1 FROM users WHERE username = %s", (username,))
            if CURSOR.fetchone():
                return False     # Meaning user does not exist

            password_hash = hash_password(password)
            CURSOR.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
            CONNECTION.commit()

            return True
        
        except Exception as e:
            print(f"Error: {e}.")
            return False
    
    
class Table:
    @staticmethod
    def create_table():
        try:
            CURSOR.execute("""                


            """)   # Treat the empty command as a placeholder. Just put smth there you want to create. The table.

            CONNECTION.commit()
            print("Table's ready!")

        except Exception as e:
            print(f"An error creating table. {e}")

table = Table()
user = User()

