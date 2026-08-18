import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "ai_manager.db")


def connect():
    conn = sqlite3.connect(DB_NAME)

    # Включаем поддержку внешних ключей
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def init_db():

    conn = connect()
    cursor = conn.cursor()

    # -----------------------------
    # ТАБЛИЦА КЛИЕНТОВ
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            phone TEXT,
            email TEXT,
            status TEXT DEFAULT 'Новый',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -----------------------------
    # ТАБЛИЦА СООБЩЕНИЙ
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (client_id)
            REFERENCES clients(id)
            ON DELETE CASCADE
        )
    """)
    
        # -----------------------------
    # ТАБЛИЦА ЗАКАЗОВ
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            client_id INTEGER NOT NULL,

            title TEXT NOT NULL,

            description TEXT,

            price REAL DEFAULT 0,

            status TEXT DEFAULT 'Новый',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (client_id)
            REFERENCES clients(id)
            ON DELETE CASCADE
        )
    """)
    
        # -----------------------------------------
    # ДОПОЛНИТЕЛЬНЫЕ ДАННЫЕ 3D-ЗАКАЗА
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            order_id INTEGER NOT NULL UNIQUE,

            model_type TEXT,
            size_cm REAL,
            material TEXT,
            color TEXT,
            production_stage TEXT,
            photo_path TEXT,

            FOREIGN KEY (order_id)
            REFERENCES orders(id)
            ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()

# =========================================================
# ДЕТАЛИ 3D-ЗАКАЗА
# =========================================================

def save_order_details(
    order_id,
    model_type=None,
    size_cm=None,
    material=None,
    color=None,
    production_stage=None
):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO order_details
        (
            order_id,
            model_type,
            size_cm,
            material,
            color,
            production_stage
        )
        VALUES (?, ?, ?, ?, ?, ?)

        ON CONFLICT(order_id)
        DO UPDATE SET
            model_type = excluded.model_type,
            size_cm = excluded.size_cm,
            material = excluded.material,
            color = excluded.color,
            production_stage = excluded.production_stage
    """, (
        order_id,
        model_type,
        size_cm,
        material,
        color,
        production_stage
    ))

    conn.commit()
    conn.close()

def get_order_details(order_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            order_id,
            model_type,
            size_cm,
            material,
            color,
            production_stage
        FROM order_details
        WHERE order_id = ?
    """, (order_id,))

    details = cursor.fetchone()

    conn.close()

    return details

# =========================================================
# КЛИЕНТЫ
# =========================================================


def add_client(name, phone=None, email=None):

    conn = connect()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO clients
            (name, phone, email)
            VALUES (?, ?, ?)
        """, (
            name,
            phone,
            email
        ))

        conn.commit()

        client_id = cursor.lastrowid

    except sqlite3.IntegrityError:

        conn.close()

        return None

    conn.close()

    return client_id


def get_client(client_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            phone,
            email,
            status,
            notes,
            created_at
        FROM clients
        WHERE id = ?
    """, (client_id,))

    client = cursor.fetchone()

    conn.close()

    return client


def find_client(name):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            phone,
            email,
            status,
            notes,
            created_at
        FROM clients
        WHERE name = ?
    """, (name,))

    client = cursor.fetchone()

    conn.close()

    return client


def search_clients(search_text):

    conn = connect()
    cursor = conn.cursor()

    search_text = search_text.strip()

    cursor.execute("""
        SELECT
            id,
            name,
            phone,
            email,
            status,
            notes,
            created_at
        FROM clients
        WHERE
            name LIKE ?
            OR phone LIKE ?
            OR email LIKE ?
        ORDER BY name
    """, (
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%"
    ))

    clients = cursor.fetchall()

    conn.close()

    return clients


def get_all_clients():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            phone,
            email,
            status,
            notes,
            created_at
        FROM clients
        ORDER BY id
    """)

    clients = cursor.fetchall()

    conn.close()

    return clients


def update_client(
    client_id,
    phone=None,
    email=None,
    status=None,
    notes=None
):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clients
        SET
            phone = ?,
            email = ?,
            status = ?,
            notes = ?
        WHERE id = ?
    """, (
        phone,
        email,
        status,
        notes,
        client_id
    ))

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated


def delete_client(client_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM clients
        WHERE id = ?
    """, (client_id,))

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted


# =========================================================
# СООБЩЕНИЯ
# =========================================================


def save_message(client_id, role, text):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages
        (client_id, role, text)
        VALUES (?, ?, ?)
    """, (
        client_id,
        role,
        text
    ))

    conn.commit()

    message_id = cursor.lastrowid

    conn.close()

    return message_id


def load_messages(client_id, limit=50):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            role,
            text,
            created_at
        FROM messages
        WHERE client_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (
        client_id,
        limit
    ))

    rows = cursor.fetchall()

    conn.close()

    rows.reverse()

    return rows


# =========================================================
# СТАТИСТИКА
# =========================================================


def get_client_stats(client_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN role = 'Клиент' THEN 1 ELSE 0 END),
            SUM(CASE WHEN role = 'Менеджер' THEN 1 ELSE 0 END),
            MAX(created_at)
        FROM messages
        WHERE client_id = ?
    """, (client_id,))

    stats = cursor.fetchone()

    conn.close()

    return stats


def get_hot_clients():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.id,
            c.name,
            COUNT(m.id) AS message_count
        FROM clients c
        LEFT JOIN messages m
            ON c.id = m.client_id
        GROUP BY c.id
        ORDER BY message_count DESC
    """)

    clients = cursor.fetchall()

    conn.close()

    return clients
    
# =========================================================
# ЗАКАЗЫ
# =========================================================


def add_order(
    client_id,
    title,
    description=None,
    price=0,
    status="Новый"
):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO orders
        (
            client_id,
            title,
            description,
            price,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        client_id,
        title,
        description,
        price,
        status
    ))

    conn.commit()

    order_id = cursor.lastrowid

    conn.close()

    return order_id


def get_order(order_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            client_id,
            title,
            description,
            price,
            status,
            created_at
        FROM orders
        WHERE id = ?
    """, (order_id,))

    order = cursor.fetchone()

    conn.close()

    return order


def get_client_orders(client_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            client_id,
            title,
            description,
            price,
            status,
            created_at
        FROM orders
        WHERE client_id = ?
        ORDER BY id DESC
    """, (client_id,))

    orders = cursor.fetchall()

    conn.close()

    return orders


def get_all_orders():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            o.id,
            o.client_id,
            c.name,
            o.title,
            o.description,
            o.price,
            o.status,
            o.created_at
        FROM orders o
        JOIN clients c
            ON o.client_id = c.id
        ORDER BY o.id DESC
    """)

    orders = cursor.fetchall()

    conn.close()

    return orders


def update_order(
    order_id,
    title=None,
    description=None,
    price=None,
    status=None
):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE orders
        SET
            title = ?,
            description = ?,
            price = ?,
            status = ?
        WHERE id = ?
    """, (
        title,
        description,
        price,
        status,
        order_id
    ))

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated


def delete_order(order_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM orders
        WHERE id = ?
    """, (order_id,))

    deleted = cursor.rowcount

    conn.commit()

    conn.close()

    return deleted

# =========================================================
# ЗАПУСК
# =========================================================

# =========================================================
# ДЕТАЛИ 3D-ЗАКАЗА
# =========================================================

def save_order_details(
    order_id,
    model_type=None,
    size_cm=None,
    material=None,
    color=None,
    production_stage=None
):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO order_details
        (
            order_id,
            model_type,
            size_cm,
            material,
            color,
            production_stage
        )
        VALUES (?, ?, ?, ?, ?, ?)

        ON CONFLICT(order_id)
        DO UPDATE SET
            model_type = excluded.model_type,
            size_cm = excluded.size_cm,
            material = excluded.material,
            color = excluded.color,
            production_stage = excluded.production_stage
    """, (
        order_id,
        model_type,
        size_cm,
        material,
        color,
        production_stage
    ))

    conn.commit()
    conn.close()


def get_order_details(order_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            order_id,
            model_type,
            size_cm,
            material,
            color,
            production_stage
        FROM order_details
        WHERE order_id = ?
    """, (order_id,))

    details = cursor.fetchone()

    conn.close()

    return details

if __name__ == "__main__":

    init_db()

    print("База данных готова.")