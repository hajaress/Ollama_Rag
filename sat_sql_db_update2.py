import sqlite3

conn = sqlite3.connect("IFB_refrigerator_service.db")
cursor = conn.cursor()

# -------------------------------
# Insert customer data
# -------------------------------
customers = [
    ('REF1001','Amit K','LG FrostFree 260L','2022-03-15','Active','Pune, Maharashtra'),
    ('REF1002','Neha Verma','Samsung TwinCool 253L','2021-07-10','Expired','Delhi'),
    ('REF1003','Rohit Mehta','Whirlpool Intellifresh 265L','2023-01-05','Active','Ahmedabad, Gujarat'),
    ('REF1004','Sneha Iyer','LG DirectCool 190L','2020-11-22','Expired','Chennai, Tamil Nadu'),
    ('REF1005','Vikas Singh','Haier HRD 195L','2022-09-18','Active','Lucknow, Uttar Pradesh')
]

cursor.executemany("""
INSERT OR IGNORE INTO customer_products
VALUES (?, ?, ?, ?, ?, ?)
""", customers)

# -------------------------------
# Insert service history
# -------------------------------
services = [
    ('REF1001','2025-06-20','Cooling issue','Gas refilled'),
    ('REF1002','2022-12-15','Compressor noise','Compressor replaced'),
    ('REF1003','2025-08-05','Ice formation','LCD Updated, Thermostat adjusted'),
    ('REF1004','2026-01-10','Door seal broken','Gasket replaced'),
    ('REF1005','2023-07-19','Not cooling','Condenser cleaned')
]

# cursor.executemany("""
# INSERT INTO service_history
# (serial_number, service_date, issue_reported, action_taken)
# VALUES (?, ?, ?, ?)
# """, services)
cursor.execute("""
INSERT INTO customer_products
VALUES (?, ?, ?, ?, ?, ?)
""", (
    "REF2001",
    "Ramesh Kumar",
    "Samsung 253L",
    "2024-01-12",
    "Active",
    "Patna, Bihar"
))


conn.commit()
print("✅ Dummy data inserted successfully")
conn.close()

