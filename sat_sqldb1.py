import sqlite3

# Create / connect to database
conn = sqlite3.connect("IFB_refrigerator_service.db")
cursor = conn.cursor()

# -------------------------------
# Create customer_products table
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS customer_products (
    serial_number TEXT PRIMARY KEY,
    customer_name TEXT,
    product_model TEXT,
    purchase_date DATE,
    warranty_status TEXT,
    address TEXT
)
""")

# -------------------------------
# Create service_history table
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS service_history (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    serial_number TEXT,
    service_date DATE,
    issue_reported TEXT,
    action_taken TEXT,
    FOREIGN KEY (serial_number) REFERENCES customer_products(serial_number)
)
""")

# Commit changes
conn.commit()

print(" Database and tables created successfully")

# Close connection
conn.close()
