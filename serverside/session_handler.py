from string import ascii_letters, digits
from secrets import choice
import json

# id_vars is a list, a result of combining
# digits (0-9) and all latin letters (a, A...)
id_vars = list(ascii_letters) + list(digits)


class Session:
    @staticmethod
    def generate_session_object(user_json):
        user_data = json.loads(user_json)

        session_obj = {
            "session_id": Session.generate_session_ID(),
            "user_id": user_data["id"],
            "username": user_data["username"],
            "password": user_data["hashed_password"],
            "level": user_data["level"],
            "coins": user_data["coins"],
            "gems": user_data["gems"],
            "platinum": user_data["platinum"],
            "fountain_claimed": user_data["fountained_claimed"],
            "title": user_data["title"]
            }
        print("Session object craeted")
        return session_obj

    @staticmethod
    def generate_session_ID():
        return "".join(choice(id_vars) for _ in range(128))


    
    
    
session = Session()
