import psycopg2
import socket
import threading
from db.table_methods import user, table
import serverside.db.global_vars.vars

CONNECTION = serverside.db.global_vars.vars.CONNECTION
CURSOR = serverside.db.global_vars.vars.CURSOR
HOST = serverside.db.global_vars.vars.HOST
PORT = serverside.db.global_vars.vars.PORT

def handle_client(conn, addr):
    print(f"[+] NEW CONNECTION [FROM {addr}].")

    welcome_message = "Welcome to the game world!\nType 'register', to create new account or 'login' to log in."
    conn.sendall(welcome_message.encode())

    while True:
        try:
            data = conn.recv(1024)

            if data == "login".encode():
                conn.sendall(b"Provide us with username & password in the format: username password")
                data = conn.recv(1024).decode().strip()
                
                parts = data.split()

                if len(parts) > 2 or len(parts) < 2:
                    conn.sendall(b"Provide exactly two arguments. Format: username password.")

                response = user.login(parts[0], parts[1])

                conn.sendall(f"{response['message']}".encode())
            
            elif data == "register".encode():
                conn.sendall(b"Provide us with username & password in the format: username password")
                data = conn.recv(1024).decode().strip()

                parts = data.split()

                if len(parts) > 2 or len(parts) < 2:
                    conn.sendall(b"Provide exactly two arguments. Format: username password")

                response = user.register(parts[0], parts[1])

                conn.sendall(f"{response['message']}".encode())

        except Exception as e:
            message = f"Error has occured! Detailed information: {e}."
            conn.sendall(message.encode())
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