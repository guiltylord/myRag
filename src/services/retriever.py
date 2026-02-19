import numpy as np

def calculate_similarity(vec1, vec2):
    """Математика: Косинусное сходство между двумя векторами."""
    # Приводим к numpy для расчетов
    v1 = np.array(vec1, dtype=np.float32)
    v2 = np.frombuffer(vec2, dtype=np.float32) if isinstance(vec2, bytes) else np.array(vec2)
    
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def get_scored_results(query_vec, db_rows):
    """Считает баллы для всех строк из БД."""
    results = []
    for text, blob in db_rows:
        score = calculate_similarity(query_vec, blob)
        results.append({"text": text, "score": score})
    # Сортируем от лучшего к худшему
    return sorted(results, key=lambda x: x["score"], reverse=True)

def apply_threshold(scored_results, threshold=0.4, top_k=3):
    """Логика 'is_enough': проверяет порог и возвращает топ-результаты или None."""
    if not scored_results or scored_results[0]["score"] < threshold:
        return None
    
    # Возвращаем только тексты топ-K результатов
    return [item["text"] for item in scored_results[:top_k]]