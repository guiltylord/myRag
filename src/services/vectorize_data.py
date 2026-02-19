from langchain_huggingface import HuggingFaceEmbeddings

# Скрытая переменная для хранения загруженной модели (Singleton)
_cached_model = None

def _get_embeddings_model():
    """
    Служебная функция: загружает модель один раз.
    При повторных вызовах просто отдает уже готовую из памяти.
    """
    global _cached_model
    if _cached_model is None:
        print("📥 [System] Загружаю модель HuggingFace (это будет только один раз)...")
        # Используем маленькую и быструю модель
        _cached_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _cached_model

def embed_text(text, model=None):
    """
    Атомарная функция: превращает одну строку в вектор.
    Можно передать модель явно (для скорости в циклах), 
    а можно не передавать (она возьмется сама).
    """
    if model is None:
        model = _get_embeddings_model()
        
    return model.embed_query(text)

def create_vectors_data(chunks):
    """
    Функция для обработки списка чанков.
    Принимает список объектов Document (от split_data).
    Возвращает список словарей для записи в БД.
    """
    vectors_data = []
    
    # Получаем ссылку на модель 1 раз перед циклом, чтобы было быстрее
    model = _get_embeddings_model()
    
    print(f"Начинаю векторизацию {len(chunks)} фрагментов...")

    for i, chunk in enumerate(chunks):
        # Передаем model внутрь, чтобы embed_text не искала её каждый раз
        vector = embed_text(chunk.page_content, model)

        vectors_data.append({
            "text": chunk.page_content, 
            "vector": vector
        })

        if (i + 1) % 10 == 0:
            print(f"Обработано {i + 1}/{len(chunks)}...")

    print("Векторизация успешно завершена.")
    return vectors_data