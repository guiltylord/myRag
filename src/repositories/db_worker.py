import sqlite3


def connect_to_db():
    """
    Открывает соединение с БД.
    """
    
    conn = sqlite3.connect("my_rag_vectors.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vector_store (
            id INTEGER PRIMARY KEY,
            text_content TEXT,
            embedding BLOB
        )
    """)

    conn.commit()
    return conn, cursor


def close_db(conn, cursor=None):
    """
    Безопасно сохраняет данные и закрывает соединение с БД.
    """
    
    
    try:
        if conn:
            conn.commit()
            if cursor:
                cursor.close()
            conn.close()
            return "БД успешно сохранена и закрыта."
    except Exception as e:
        return f"Ошибка при закрытии БД: {e}"

def fetch_all_embeddings(cursor):
    """Достает все тексты и векторы из БД."""


    cursor.execute("SELECT text_content, embedding FROM vector_store")
    return cursor.fetchall()
