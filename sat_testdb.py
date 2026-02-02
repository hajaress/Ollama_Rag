import sqlite3

conn = sqlite3.connect("./IFB_refrigerator_service.db")
cursor_1 = conn.cursor()
cursor_2 = conn.cursor()
cursor_1.execute("""
SELECT name FROM sqlite_master
WHERE type='table';
""")
cursor_2.execute("SELECT * FROM customer_products")
rows = cursor_2.fetchall()
print("Customer Products:", rows)
tables = cursor_1.fetchall()
print("Tables found:", tables)

conn.close()
