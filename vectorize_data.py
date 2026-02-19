from langchain_huggingface import HuggingFaceEmbeddings

default_embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_vectors_data(chunks, embeddings_model=default_embeddings_model):
    """
    Принимает текстовые чанки (объекты LangChain Document) и модель.
    Возвращает список словарей с текстом и сырым вектором.
    """
    vectors_data = []

    print(f"Начинаю векторизацию {len(chunks)} фрагментов...")

    for i, chunk in enumerate(chunks):
        # Генерируем вектор через LangChain метод .embed_query
        # Он возвращает обычный список (list) из float чисел
        vector = embeddings_model.embed_query(chunk.page_content)

        # Сохраняем в промежуточный список
        vectors_data.append({"text": chunk.page_content, "vector": vector})

        if (i + 1) % 10 == 0:
            print(f"Обработано {i + 1}/{len(chunks)}...")

    print("Векторизация успешно завершена.")
    return vectors_data
