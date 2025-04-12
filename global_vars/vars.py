import psycopg2

CONNECTION = psycopg2.connect(
    dbname = "game_db",
    user = "game_db_user",
    password = "grubasek1",
    host = "0.0.0.0",
    port = 5432
)

CURSOR = CONNECTION.cursor()
HOST = "127.0.0.1"
PORT = 65432