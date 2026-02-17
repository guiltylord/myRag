import sqlite3

import numpy as np

# 1. Подключаемся к файлу базы данных (или создаем его)
conn = sqlite3.connect("my_rag_vectors.db")
cursor = conn.cursor()

# 2. Создаем таблицу
cursor.execute("""
    CREATE TABLE IF NOT EXISTS vector_store (
        id INTEGER PRIMARY KEY,
        text_content TEXT,
        embedding BLOB
    )
""")

# 3. Превращаем текст в векторы и сохраняем в БД
for chunk in chunks:
    # Генерируем вектор
    vector = embeddings_model.embed_query(chunk.page_content)
    # Конвертируем список чисел в байты для хранения в SQLite
    vector_blob = np.array(vector, dtype=np.float32).tobytes()

    cursor.execute(
        "INSERT INTO vector_store (text_content, embedding) VALUES (?, ?)",
        (chunk.page_content, vector_blob),
    )

conn.commit()
print("Все фрагменты успешно сохранены в SQLite.")
print("Все фрагменты успешно сохранены в SQLite.")
