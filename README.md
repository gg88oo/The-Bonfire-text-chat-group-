# 🔥 Bonfire Chat

A real-time anonymous chat application built with Flask and SQLite. Users can register, login, and post messages that appear instantly for everyone.

## ✨ Features

- User registration and login
- Password hashing for security
- Real-time message updates
- Persistent message history
- Clean, simple interface
- Session management

## 📋 Requirements

- Python 3.6 or higher
- Flask
- Flask-Session
- CS50 library (for SQLite)
- Werkzeug

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/bonfire-chat.git
cd bonfire-chat

# Install dependencies
pip install flask flask-session cs50 werkzeug

# Initialize the database
python
>>> import sqlite3
>>> conn = sqlite3.connect('bonfire.db')
>>> conn.execute('''
... CREATE TABLE IF NOT EXISTS users (
...     user_id INTEGER PRIMARY KEY AUTOINCREMENT,
...     username TEXT NOT NULL UNIQUE,
...     password_hash TEXT NOT NULL
... )''')
>>> conn.execute('''
... CREATE TABLE IF NOT EXISTS messages (
...     id INTEGER PRIMARY KEY AUTOINCREMENT,
...     user_id INTEGER NOT NULL,
...     username TEXT NOT NULL,
...     message TEXT NOT NULL,
...     date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
... )''')
>>> conn.commit()
>>> conn.close()

# Run the app
python app.py
