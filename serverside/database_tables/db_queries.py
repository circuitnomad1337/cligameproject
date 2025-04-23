SELECT_PASSWORD = "SELECT password_hash FROM users WHERE username = %s"
EXTRACT_USER_DATA = "SELECT * FROM users WHERE username = %s"
CREATE_USER = "INSERT INTO users (username, password_hash) VALUES (%s, %s);"