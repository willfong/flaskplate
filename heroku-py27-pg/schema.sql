CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  username VARCHAR(100),
  password VARCHAR(100),
  joined TIMESTAMPTZ DEFAULT NOW()
);
CREATE UNIQUE INDEX udx_username ON users (username);
CREATE INDEX idx_joined ON users (joined);
INSERT INTO users ( username, password ) VALUES ( 'username', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');
