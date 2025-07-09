# backend.py
from flask import Flask, request, jsonify, render_template
import sqlite3
import time
import hashlib
import hmac
import os

app = Flask(__name__)
DB_NAME = 'keyrush_market.db'

# === Проверка подписи от Telegram ===
def check_telegram_auth(data, bot_token):
    auth_data = data.copy()
    hash_received = auth_data.pop('hash')
    data_check_string = '\n'.join([f"{k}={auth_data[k]}" for k in sorted(auth_data)])
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return hmac_hash == hash_received

@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    bot_token = os.environ.get("BOT_TOKEN")

    if not check_telegram_auth(data, bot_token):
        return jsonify({"error": "Authentication failed"}), 403

    telegram_id = data['id']
    username = data.get('username', '')
    full_name = data.get('first_name', '') + ' ' + data.get('last_name', '')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    existing = cursor.fetchone()

    if not existing:
        cursor.execute("INSERT INTO users (telegram_id, username, full_name, created_at) VALUES (?, ?, ?, ?)", (
            telegram_id, username, full_name, int(time.time())
        ))
        conn.commit()

    conn.close()
    return jsonify({"ok": True})

@app.route('/profile/<int:telegram_id>')
def profile(telegram_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user[0],
        "telegram_id": user[1],
        "username": user[2],
        "full_name": user[3],
        "created_at": user[4]
    })

if __name__ == '__main__':
    app.run(debug=True)
