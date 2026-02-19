import numpy as np


def save_vectors(conn, cursor, vectors_data):
    """
    Принимает подготовленные данные и загружает их в БД.
    """


    prepared_rows = []

    for item in vectors_data:
        vector_blob = np.array(item["vector"], dtype=np.float32).tobytes()
        prepared_rows.append((item["text"], vector_blob))

    cursor.executemany(
        "INSERT INTO vector_store (text_content, embedding) VALUES (?, ?)",
        prepared_rows,
    )
    conn.commit()
    print(f"Загрузка завершена. В базу добавлено {len(prepared_rows)} записей.")
