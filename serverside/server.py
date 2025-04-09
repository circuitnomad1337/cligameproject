import psycopg2
import socket
import threading
from db.table_methods import User, Table

CONNECTION = psycopg2.connect(
    dbname = "game_db",
    user = "game_db_user",
    password = "",
    host = "0.0.0.0",
    port = 5432
)

CURSOR = CONNECTION.cursor()
HOST = "127.0.0.1"
PORT = 65432

def handle_client(conn, addr):
    print(f"[+] NEW CONNECTION [FROM {addr}].")

    welcome_message = "Welcome to the game world!\nType 'register', to create new account or 'login' to log in."
    conn.sendall(welcome_message.encode())

    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            
            conn.sendall(f"You chose: {data}\n".encode())

        except Exception as e:
            break

    print(f"[-] CONNECTION TERMINATED [WITH {addr}].")
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER] listening on [{HOST}:{PORT}].")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()