LOGIN = "SELECT password_hash FROM users WHERE username = %s"
SEARCH_USERNAME = "SELECT 1 FROM users WHERE username = %s"
REGISTER_USER = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"