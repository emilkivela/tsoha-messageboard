CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE topics(
    id SERIAL PRIMARY KEY,
    name TEXT,
    creator INTEGER REFERENCES users ON DELETE CASCADE,
    created_at TIMESTAMP
)

CREATE TABLE threads(
    id SERIAL PRIMARY KEY,
    name TEXT,
    topic INTEGER REFERENCES topics ON DELETE CASCADE,
    creator INTEGER REFERENCES users ON DELETE CASCADE,
    created_at TIMESTAMP
);

CREATE TABLE messages(
    id SERIAL PRIMARY KEY,
    content TEXT,
    thread INTEGER REFERENCES threads ON DELETE CASCADE,
    author INTEGER REFERENCES users ON DELETE CASCADE,
    sent_at TIMESTAMP
);

CREATE TABLE directs(
    id SERIAL PRIMARY KEY,
    content TEXT,
    author INTEGER REFERENCES users ON DELETE CASCADE,
    receiver INTEGER REFERENCES users ON DELETE CASCADE,
    sent_at TIMESTAMP
);