import sqlite3


def connect_to_db():
    conn = sqlite3.connect("my_rag_vectors.db")
    cursor = conn.cursor()

    # Создаем таблицу
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vector_store (
            id INTEGER PRIMARY KEY,
            text_content TEXT,
            embedding BLOB
        )
    """)

    conn.commit()
    return conn, cursor  # <--- Возвращаем кортеж из двух объектов


def close_db(conn, cursor=None):
    """
    Безопасно сохраняет данные и закрывает соединение с БД.
    """
    try:
        if conn:
            # 1. Финальный сейв на всякий случай
            conn.commit()

            # 2. Закрываем курсор, если он передан
            if cursor:
                cursor.close()

            # 3. Закрываем само соединение
            conn.close()
            return "БД успешно сохранена и закрыта."
    except Exception as e:
        return f"Ошибка при закрытии БД: {e}"
