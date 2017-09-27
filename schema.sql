DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username TEXT,
  password TEXT
);

INSERT INTO users ( username, password ) VALUES ( 'username', 'password');
