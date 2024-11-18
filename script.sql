/*CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('ops', 'client')) NOT NULL,
    verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    uploaded_by INTEGER NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_type TEXT NOT NULL CHECK(file_type IN ('pptx', 'docx', 'xlsx')),
    FOREIGN KEY (uploaded_by) REFERENCES users (id)
);/*
