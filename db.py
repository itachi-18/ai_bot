import sqlite3


def get_faq_answer(question_query):
    conn = sqlite3.connect("database/faq.db")
    cursor = conn.cursor()
    # Simple keyword search for MVP
    cursor.execute(
        "SELECT answer FROM faqs WHERE question LIKE ?", (f"%{question_query}%",)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
