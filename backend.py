from flask import Flask, request, jsonify
import hashlib
import hmac
import time
import sqlite3
import os

app = Flask(__name__)
DB_NAME = 'keyrush_market.db'  # Имя вашей базы, можно поменять

BOT_TOKEN = os.environ.get('BOT_TOKEN', 'ВАШ_ТОКЕН_БОТА')  # Поставьте токен вашего бота сюда или через env

# Проверка подписи Telegram Login Widget
def check_telegram_auth(data, bot_token):
    auth_data = data.copy()
    hash_received = auth_data.pop('hash', None)
    data_check_string = '\n'.join(f"{k}={auth_data[k]}" for k in sorted(auth_data))
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return hmac_hash == hash_received and (time.time() - int(auth_data.get('auth_date', 0))) < 86400

@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400

    if not check_telegram_auth(data, BOT_TOKEN):
        return jsonify({"error": "Authentication failed"}), 403

    telegram_id = data.get('id')
    username = data.get('username', '')
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    full_name = f"{first_name} {last_name}".strip()

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            full_name TEXT,
            created_at INTEGER
        )
    ''')
    c.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
    user = c.fetchone()

    if not user:
        c.execute("INSERT INTO users (telegram_id, username, full_name, created_at) VALUES (?, ?, ?, ?)",
                  (telegram_id, username, full_name, int(time.time())))
        conn.commit()
    conn.close()

    return jsonify({"ok": True})

@app.route('/profile/<int:telegram_id>')
def profile(telegram_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT telegram_id, username, full_name, created_at FROM users WHERE telegram_id = ?", (telegram_id,))
    user = c.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "telegram_id": user[0],
        "username": user[1],
        "full_name": user[2],
        "created_at": user[3]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

