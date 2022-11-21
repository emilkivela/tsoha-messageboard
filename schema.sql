CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE threads(
    id SERIAL PRIMARY KEY,
    name TEXT,
    creator INTEGER REFERENCES users,
    created_at TIMESTAMP
);

CREATE TABLE messages(
    id SERIAL PRIMARY KEY,
    content TEXT,
    thread INTEGER REFERENCES threads,
    author INTEGER REFERENCES users,
    sent_at TIMESTAMP
);

CREATE TABLE directs(
    id SERIAL PRIMARY KEY,
    content TEXT,
    author INTEGER REFERENCES users,
    receiver INTEGER REFERENCES users,
    sent_at TIMESTAMP
);