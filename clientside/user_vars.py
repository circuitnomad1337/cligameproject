import os

DOCUMENTS_DIR = os.path.join(os.path.expanduser("~"), "Documents")
os.makedirs(DOCUMENTS_DIR, exist_ok = True)
SESSION_FILE = os.path.join(DOCUMENTS_DIR, "CLIGAME_session.json")

HOST, PORT = "127.0.0.1", 65432

LOG_FROM_SES = "We're logging you from session..."
LOG_OR_REG = "Do you want to log in or register? Type it here (login/register): "
UNKNOWN_ACTION = 'Unknown action. Type either "login" or "register".'

DEMAND_USERNAME = "Your login: "
DEMAND_PASSWORD = "Your password: "

