import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "refrigerator_service.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def get_customer_by_serial(serial_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT serial_number, customer_name, product_model,
           purchase_date, warranty_status, address
    FROM customer_products
    WHERE serial_number = ?
    """, (serial_number,))

    row = cursor.fetchone()
    conn.close()
    return row
