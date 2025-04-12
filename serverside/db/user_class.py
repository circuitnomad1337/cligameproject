import serverside.global_vars.db_queries as db_queries
import serverside.global_vars.ret_messages as ret_mes
import serverside.global_vars.vars as vars
import hashlib



def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class User:
    @staticmethod
    def login(username, password):
        try:
            vars.CURSOR.execute(db_queries.LOGIN, (username,))
            result = vars.CURSOR.fetchone()

            if not result or hash_password(password) != result[0]:
                return {"bool": False, "message": f"{ret_mes.ERROR_LOG_IN}"}
            else:
                return {"bool": True, "message": f"{ret_mes.SUCCESSFUL_LOGIN}{username}!"}
            
        except Exception as e:
            return {"bool": False, "mesage": e}
        
    
    @staticmethod
    def register(username, password):
        try:
            vars.CURSOR.execute(db_queries.SEARCH_USERNAME, (username,))
            if vars.CURSOR.fetchone():
                return {"bool": False, "message": ret_mes.USERNAME_TAKEN}
            
            else:
                password_hash = hash_password(password)
                
                try:
                    vars.CURSOR.execute(db_queries.REGISTER_USER, (
                                        (username, password_hash)))
                    vars.CONNECTION.commit()
                    return {"bool": True, 
                            "message": f"{username} {ret_mes.SUCCESSFUL_REG}!".capitalize()}
                
                except Exception as e:
                    vars.CONNECTION.rollback()
                    return {"bool": False, "message": e}
                
        except Exception as e:
            vars.CONNECTION.rollback()
            return {"bool": False, "message": e}
        





user = User()