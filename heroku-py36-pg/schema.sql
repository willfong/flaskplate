CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  username VARCHAR(100),
  password VARCHAR(64),
  joined TIMESTAMPTZ DEFAULT NOW()
);
CREATE UNIQUE INDEX udx_username ON users (username);
CREATE INDEX idx_joined ON users (joined);

CREATE TABLE lists (
  id BIGSERIAL PRIMARY KEY,
  users_id BIGINT,
  name VARCHAR(100),
  created TIMESTAMPTZ DEFAULT NOW()
);
CREATE UNIQUE INDEX idx_usersid_name ON lists (users_id, name);

CREATE TABLE list_items (
  id BIGSERIAL PRIMARY KEY,
  lists_id BIGINT,
  name VARCHAR(100)
);
CREATE INDEX idx_listsid ON list_items (lists_id);
