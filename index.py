from flask import Flask, request, jsonify
import sqlite3
import os
import bcrypt
from datetime import datetime
import hashlib

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DB_FILE = 'user.db'

def execute_query(query, params=()):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor


def encrypt_url(data):
    """Generate a secure encrypted string."""
    return hashlib.sha256(data.encode()).hexdigest()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    try:
        execute_query(
            "INSERT INTO users (username, email, password, role, verified) VALUES (?, ?, ?, ?, ?)",
            (data['username'], data['email'], hashed_password.decode('utf-8'), 'client', False),
        )
        encrypted_url = encrypt_url(data['email'])
        return jsonify({'message': 'User registered successfully', 'encrypted_url': encrypted_url}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Email already exists'}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = execute_query("SELECT * FROM users WHERE email = ?", (data['email'],)).fetchone()
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user[3].encode('utf-8')):
        return jsonify({'message': 'Login successful', 'role': user[4]}), 200
    return jsonify({'message': 'Invalid email or password'}), 401


@app.route('/upload', methods=['POST'])
def upload_file():
    user_id = request.headers.get('User-ID')  # Pass user ID in headers for simplicity
    user = execute_query("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user or user[4] != 'ops':
        return jsonify({'message': 'Only Ops Users can upload files'}), 403

    file = request.files['file']
    if file and file.filename.split('.')[-1] in ['pptx', 'docx', 'xlsx']:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        execute_query(
            "INSERT INTO files (file_name, file_path, uploaded_by, file_type) VALUES (?, ?, ?, ?)",
            (file.filename, file_path, user_id, file.filename.split('.')[-1]),
        )
        return jsonify({'message': 'File uploaded successfully'}), 201
    return jsonify({'message': 'Invalid file type'}), 400


@app.route('/list', methods=['GET'])
def list_files():
    files = execute_query("SELECT id, file_name, uploaded_at FROM files").fetchall()
    return jsonify(
        [{'id': f[0], 'file_name': f[1], 'uploaded_at': f[2]} for f in files]
    )


@app.route('/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    user_id = request.headers.get('User-ID')  # Pass user ID in headers for simplicity
    user = execute_query("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user or user[4] != 'client':
        return jsonify({'message': 'Only Client Users can download files'}), 403

    file = execute_query("SELECT file_path FROM files WHERE id = ?", (file_id,)).fetchone()
    if file:
        encrypted_url = encrypt_url(file[0])
        return jsonify({'download_url': f'/secure_download/{encrypted_url}'}), 200
    return jsonify({'message': 'File not found'}), 404


@app.route('/secure_download/<string:encrypted_url>', methods=['GET'])
def secure_download(encrypted_url):
    file = execute_query("SELECT file_path FROM files").fetchall()
    for f in file:
        if encrypt_url(f[0]) == encrypted_url:
            return jsonify({'message': f'Securely download file from {f[0]}'}), 200
    return jsonify({'message': 'Invalid or expired URL'}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
