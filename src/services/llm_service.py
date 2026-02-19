import ollama

def build_prompt(query, context_chunks=None):
    """
    Собирает финальную строку промпта.
    """
    if not context_chunks:
        # Если контекста нет, просто отдаем вопрос
        return f"Question: {query}\nAnswer:"
    
    # Если контекст есть, склеиваем его
    context_text = "\n---\n".join(context_chunks)
    
    # Системный промпт для RAG
    return (
        f"You are a helpful assistant. Use the following context to answer the question.\n"
        f"Context:\n{context_text}\n\n"
        f"Question: {query}\n"
        f"Answer:"
    )

def call_llm(prompt):
    """
    Отправляет промпт в локальную LLM (модель phi3:mini).
    """
    try:
        print("⏳ Генерирую ответ через Phi-3...")
        
        # stream=False означает, что мы ждем полный ответ, а не по буквам
        response = ollama.generate(model='phi3:mini', prompt=prompt, stream=False)
        
        return response['response']
        
    except Exception as e:
        return f"Ошибка при вызове LLM: {e}. Убедись, что LLM запущена!"