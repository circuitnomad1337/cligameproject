from serverside.db.user_class import user

import global_vars.ret_messages as ret_mes
import global_vars.vars as vars
import threading
import socket


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
    server.bind((vars.HOST, vars.PORT))
    server.listen()

    print(f"[SERVER] listening on [{vars.HOST}:{vars.PORT}].")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()