-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,            -- Внутренний ID
    telegram_id INTEGER UNIQUE NOT NULL,             -- Telegram ID
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    photo_url TEXT,
    auth_date INTEGER,
    role TEXT DEFAULT 'buyer',                       -- buyer, seller, mod, admin, owner
    rating REAL DEFAULT 5.0,
    is_banned INTEGER DEFAULT 0
);

-- Таблица товаров (игр)
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER NOT NULL,                      -- user.id
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,                          -- цена в минимальных единицах (например, Stars * 100)
    currency TEXT NOT NULL,                          -- 'TON' или 'XTR'
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES users(id)
);

-- Таблица ключей для товаров
CREATE TABLE IF NOT EXISTS product_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    game_key TEXT NOT NULL,
    is_sold INTEGER DEFAULT 0,
    buyer_id INTEGER,
    sold_at TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (buyer_id) REFERENCES users(id)
);

-- Таблица сделок (транзакций)
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    price INTEGER,
    currency TEXT,
    status TEXT DEFAULT 'success',                   -- success, refunded, disputed
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Таблица жалоб
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    message TEXT,
    status TEXT DEFAULT 'open',                      -- open, resolved, declined
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    resolved_by INTEGER,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id),
    FOREIGN KEY (buyer_id) REFERENCES users(id),
    FOREIGN KEY (seller_id) REFERENCES users(id),
    FOREIGN KEY (resolved_by) REFERENCES users(id)
);

-- Таблица сообщений в чате поддержки
CREATE TABLE IF NOT EXISTS support_chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    sent_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (complaint_id) REFERENCES complaints(id),
    FOREIGN KEY (sender_id) REFERENCES users(id)
);

-- Лог действий
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
