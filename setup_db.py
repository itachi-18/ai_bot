import sqlite3

conn = sqlite3.connect("database/faq.db")
cursor = conn.cursor()

# Create Table
cursor.execute(
    """CREATE TABLE IF NOT EXISTS faqs 
               (id INTEGER PRIMARY KEY, question TEXT, answer TEXT)"""
)

# Add Sample Data
faqs = [
    ("shipping", "We ship worldwide within 5-7 business days."),
    ("refund", "Our refund policy covers 30 days with a receipt."),
    ("contact", "You can reach us at support@ai-startup.com"),
]

cursor.executemany("INSERT INTO faqs (question, answer) VALUES (?, ?)", faqs)
conn.commit()
conn.close()
print("Database initialized successfully!")
