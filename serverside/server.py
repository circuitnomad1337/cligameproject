from serverside.db.user_class import user

import global_vars.server_messages as srv_mes
import global_vars.ret_messages as ret_mes
import global_vars.vars as vars
import threading
import socket


def log_reg(conn, instr):
    conn.sendall(srv_mes.LOGREG_DATA_DEMAND)
    data = conn.recv(1024).decode().strip()
    parts = data.split()

    if len(parts) != 2:
        conn.sendall(srv_mes.WRONG_LOGIN_DATA_FORMAT)
        return


    if instr == "login":
        response = user.login(parts[0], parts[1])
        retmes = response["message"].encode()
        conn.sendall(retmes)

    elif instr == "register":
        response = user.register(parts[0], parts[1])
        retmes = response["message"].encode()
        conn.sendall(retmes)

    else:
        conn.sendall(srv_mes.UNKNOWN_INSTRUCTION)
        return

def handle_client(conn, addr):
    print(f"{srv_mes.NEW_CONNECTION}[{addr}]")
    conn.sendall(srv_mes.WELCOME_MESSAGE)

    while True:
        try:
            data = conn.recv(1024).decode().strip()
            
            if data == "login" or data == "register":
                log_reg(conn, data)
            else:
                conn.sendall(srv_mes.UNKNOWN_INSTRUCTION)

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