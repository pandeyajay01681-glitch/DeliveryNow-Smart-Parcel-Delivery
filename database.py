
import sqlite3
import uuid
from datetime import datetime

DB_NAME = "delivery.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def create_table():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_id TEXT UNIQUE,
            customer TEXT,
            phone TEXT,
            pickup TEXT,
            destination TEXT,
            package TEXT,
            weight REAL,
            delivery_type TEXT,
            delivery_date TEXT,
            delivery_time TEXT,
            price REAL,
            status TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_booking(data):
    conn = get_connection()
    tracking_id = "DN" + uuid.uuid4().hex[:8].upper()

    conn.execute("""
        INSERT INTO bookings (
            tracking_id, customer, phone, pickup,
            destination, package, weight, delivery_type,
            delivery_date, delivery_time, price,
            status, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        tracking_id,
        data["customer"],
        data["phone"],
        data["pickup"],
        data["destination"],
        data["package"],
        data["weight"],
        data["delivery_type"],
        data["delivery_date"],
        data["delivery_time"],
        data["price"],
        "Booked",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return tracking_id


def get_booking(tracking_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    result = conn.execute(
        "SELECT * FROM bookings WHERE tracking_id = ?",
        (tracking_id,)
    ).fetchone()

    conn.close()
    return dict(result) if result else None


def get_all_bookings():
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    result = conn.execute(
        "SELECT * FROM bookings ORDER BY id DESC"
    ).fetchall()

    conn.close()
    return [dict(row) for row in result]


def update_status(tracking_id, status):
    conn = get_connection()

    conn.execute(
        "UPDATE bookings SET status = ? WHERE tracking_id = ?",
        (status, tracking_id)
    )

    conn.commit()
    conn.close()
