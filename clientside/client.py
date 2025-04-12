import socket

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    data = s.recv(1024).decode()
    print(data)

    msg = input()
    msg = msg.encode()
    s.sendall(msg)

    data = s.recv(1024).decode()
    print(data)

    msg = input()
    s.sendall(msg.encode())

    data = s.recv(1024).decode()
    print(data)

        