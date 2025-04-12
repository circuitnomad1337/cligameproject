from serverside.db.user_class import user

import global_vars.server_messages as srv_mes
import global_vars.ret_messages as ret_mes
import global_vars.vars as vars
import threading
import socket


def handle_client(conn, addr):
    print(f"{srv_mes.NEW_CONNECTION}[{addr}]")

    conn.sendall(srv_mes.WELCOME_MESSAGE)

    while True:
        try:
            data = conn.recv(1024)

            if data == "login".encode():
                conn.sendall(srv_mes.LOGREG_DATA_DEMAND)
                data = conn.recv(1024).decode().strip()
                
                parts = data.split()

                if len(parts) > 2 or len(parts) < 2:
                    conn.sendall(srv_mes.WRONG_LOGIN_DATA_FORMAT)

                response = user.login(parts[0], parts[1])
                ret_sendall = response["message"].encode()
                conn.sendall(ret_sendall)
            
            elif data == "register".encode():
                conn.sendall(srv_mes.LOGREG_DATA_DEMAND)
                data = conn.recv(1024).decode().strip()

                parts = data.split()

                if len(parts) > 2 or len(parts) < 2:
                    conn.sendall(srv_mes.WRONG_LOGIN_DATA_FORMAT)

                response = user.login(parts[0], parts[1])
                ret_sendall = response["message"].encode()
                conn.sendall(ret_sendall)

        except Exception as e:
            conn.sendall(f"{e}".encode())
            break

    print(f"{srv_mes.CONNECTION_TERMINATED}[{addr}]")
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((vars.HOST, vars.PORT))
    server.listen()

    print(f"{srv_mes.SERVER_LISTENING}[{vars.HOST}:{vars.PORT}]")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()