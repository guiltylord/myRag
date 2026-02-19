from langchain_huggingface import HuggingFaceEmbeddings

_cached_model = None

def _get_embeddings_model():
    """
    Умная функция: загружает модель один раз.
    При повторных вызовах просто отдает уже готовую.
    """
    global _cached_model
    if _cached_model is None:
        print("📥 [System] Загружаю модель (это будет только один раз)...")
        _cached_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _cached_model

def embed_text(text, model=None):
    """
    Атомарная функция: превращает одну строку в вектор.
    Модель можно передать. Если не передал — она возьмется сама.
    """


    if model is None:
        model = _get_embeddings_model()
        
    return model.embed_query(text)

def create_vectors_data(chunks):
    """
    Функция для обработки списка чанков.
    """


    vectors_data = []
    model = _get_embeddings_model()
    print(f"Начинаю векторизацию {len(chunks)} фрагментов...")

    for i, chunk in enumerate(chunks):
        vector = embed_text(chunk.page_content, model)

        vectors_data.append({"text": chunk.page_content, "vector": vector})

        if (i + 1) % 10 == 0:
            print(f"Обработано {i + 1}/{len(chunks)}...")

    print("Векторизация успешно завершена.")
    return vectors_data