from database_tables.user_table import user
import socket, threading, variables, json
import signal, sys, time, os

class Server:
    def __init__(self, host=variables.HOST, port=variables.PORT):
        self.host = host
        self.port = port
        self.server_socket = None

        self.routes = {
            "login": user.login_user,
            "register": user.register_user
        }

    def host_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))

            return "Server created!"
        
        except Exception as e:
            return e

    def start_server(self):
        if not self.server_socket:
            return "Lacking server socket."

        try:
            self.server_socket.listen()

            while True:
                client_socket, client_address = self.server_socket.accept()
                active_conns.append(client_socket)
                self.handle_client(client_socket)

        except Exception as e:
            return e

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(4096).decode()

            if data:
                client_thread = threading.Thread(target=self.route_handler, args=(client_socket, data))
                client_thread.start()

        except Exception as e:
            return e
        
    def route_handler(self, conn, data):
        try:
            data_dict = json.loads(data)
            action = data_dict.get("action")

            if not action:
                conn.sendall(b"Missing 'action' in request.")
                return

            handler = self.routes.get(action)

            if handler:
                conn.sendall(handler(conn, data_dict))

            else:
                conn.sendall(f"Unknown action: {action}".encode())

        except Exception as e:
            conn.sendall(b"Server error")

active_conns = []

def handle_ctrlz(signal_num, frame):
    print("CTRL-Z pressed! Shutting down...")
    
    for conn in active_conns:
        try:
            conn.close()
            print(f"{conn} closed.")

        except Exception as e:
            print(e)

    sys.exit(0)

signal.signal(signal.SIGTSTP, handle_ctrlz)

if __name__ == "__main__":
    server = Server()
    server.host_server()
    server.start_server()