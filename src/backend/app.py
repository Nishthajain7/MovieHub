from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3 
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'your_secret_key'

USERNAME = 'admin'
PASSWORD = 'a123'

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS USERS (
                name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                whatsapp TEXT NOT NULL,
                dob TEXT NOT NULL,
                genres TEXT NOT NULL,
                password TEXT NOT NULL)""")    
    print("made")
    conn.commit()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')
    whatsapp = data.get('whatsapp')
    dob = data.get('dob')
    genres = data.get('genres')
    password = data.get('password')

    if not name or not username or not password:
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO USERS (name, username, email, phone, whatsapp, dob, genres, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(name, username, email, phone, whatsapp, dob, genres, password))
        conn.commit()
        print("User successfully registered:", name, username)
        return jsonify({"status": "success", "message": "Registration successful"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "Username already exists"}), 409


@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USERS WHERE username = ? AND password = ?",(username, password))
    user = cursor.fetchone()

    if user:
        session['username'] = user[1]
        session['name'] = user[0]
        session['email'] = user[2]
        session['phone'] = user[3]
        session['whatsapp'] = user[4]
        session['dob'] = user[5]
        session['genres'] = user[6]
        return jsonify({"status": "success", "message": "Login successful"})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route('/profile', methods=['GET'])
def profile():
    if 'username' not in session:
        return jsonify({"status": "error", "message": "Not logged in"}), 401
    
    return jsonify({
        "status": "success",
        "name": session.get('name'),
        "username": session.get('username'),
        "email": session.get('email'),
        "phone": session.get('phone'),
        "whatsapp": session.get('whatsapp'),
        "dob": session.get('dob'),
        "genres": session.get('genres')
    })


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return jsonify({"status": "success", "message": "Logged out"})

@app.route('/', methods=['GET'])
def check_login():
    if 'username' in session:
        return jsonify({"status": "success", "message": f"Logged in as {session['username']}"})
    return jsonify({"status": "error", "message": "Not logged in"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)