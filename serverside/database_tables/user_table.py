from database_tables import db_queries
from session_handler import session
import variables as variables
import hashlib, json

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class User:
    @staticmethod
    def login_user(conn, data_dict):
        username = data_dict.get("username")
        password = data_dict.get("password")

        try:
            variables.CURSOR.execute(db_queries.SELECT_PASSWORD, (username,))
            data = variables.CURSOR.fetchone()
            if not data:
                print(variables.USER_NOT_FOUND)

            if data[0] == password :
                ret = {
                    "action_result": variables.USER_LOGGED_IN
                }
    
                return json.dumps(ret).encode() 
            
            elif data[0] == hash_password(password):
                session_obj = session.generate_session_object(User.extract_user_data(username))
                ret = {
                    "action_result": variables.USER_LOGGED_IN,
                    "session_obj": session_obj
                }

                return json.dumps(ret).encode()

            else:
                conn.sendall(b"Wrong password!")
            
        except Exception as e:
            print("EXCEPTION login_user", e)

    @staticmethod
    def register_user(conn, data_dict):
        username = data_dict.get("username")
        password = data_dict.get("password")
        hashed_password = hash_password(password)

        try:
            variables.CURSOR.execute(db_queries.CREATE_USER, (username, hashed_password))
            variables.CONNECTION.commit()
            session_obj = session.generate_session_object(User.extract_user_data(username))

            ret = {
                "action_result": variables.USER_CREATED,
                "session_obj": session_obj
            }

            return json.dumps(ret).encode()

        except Exception as e:
            print("EXCEPTION register_ user", e)
            variables.CONNECTION.rollback()
            return False

    @staticmethod
    def extract_user_data(username):
        try:
            variables.CURSOR.execute(db_queries.EXTRACT_USER_DATA, (username,))
            data = variables.CURSOR.fetchone()

            if data:
                ret = {
                    "id": data[0],
                    "username": data[1],
                    "hashed_password": data[2],
                    "level": data[3],
                    "coins": data[4],
                    "gems": data[5],
                    "platinum": data[6],
                    "fountained_claimed": data[7],
                    "title": data[8]
                }

                return json.dumps(ret)
            
        except Exception as e:
            print("EXCEPTION extract_user_data, ", e)
            return
        
user = User()

# 20.04 trzeba zmienic caly ten kod w huuj