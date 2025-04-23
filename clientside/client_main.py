import user_vars, socket, json, os

def connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((user_vars.HOST, user_vars.PORT))
    return client_socket

def collect_inputLOG_data(action):

    username = input(user_vars.DEMAND_USERNAME)
    password = input(user_vars.DEMAND_PASSWORD)

    login_dict = {
        "action": action,
        "username": username,
        "password": password
    }

    return login_dict

def save_session_object(session_object):
    data = json.loads(session_object)
    session_data = data["session_obj"]
    try:
        with open(user_vars.SESSION_FILE, "w") as f:
            json.dump(session_data, f, indent = 4)

        print("Session saved")

    except Exception as e:
        print("error saving a session obj!")

def client_login(client_socket, action):
    login_data = collect_inputLOG_data(action)
    login_data_encoded = json.dumps(login_data).encode()

    client_socket.sendall(login_data_encoded)

    while True:
        rcv_data = client_socket.recv(4096).decode()
        save_session_object(rcv_data)

def login_from_saved_session(client_socket, action):
    print(user_vars.LOG_FROM_SES)

    try:
        with open(user_vars.SESSION_FILE, "r") as f:
            retdata = json.load(f)

            login_data = {"action": action,
                          "username": retdata["username"],
                          "password": retdata["password"]
                        }
            json_dump = json.dumps(login_data).encode()
            
            client_socket.sendall(json_dump)

            while True:
                rcv_data = client_socket.recv(4096).decode()
                print(rcv_data)

    except Exception as e:
        print("EXCEPTION LOG_FROM_SESSION", e)

def register(client_socket, action):
    data = collect_inputLOG_data(action)
    jsonified_data = json.dumps(data).encode()

    client_socket.sendall(jsonified_data)

    while True:
        rcv_data = client_socket.recv(4096).decode()
        save_session_object(rcv_data)
        print("sesion made!")




if __name__ == "__main__":
    action = input(user_vars.LOG_OR_REG).lower()
    conn = connect()

    if action == "login":
        if os.path.exists(user_vars.SESSION_FILE):
            login_from_saved_session(conn, action)

        else:
            client_login(conn, action)

    elif action == "register":
        register(conn, action)

    else:
        print(user_vars.UNKNOWN_ACTION)