import ollama
def build_prompt(query, context_chunks=None):
    """
    Собирает финальную строку промпта.
    """


    if not context_chunks:
        return (
            f"You are a strict assistant. The user will ask a question. "
            f"If you don't have specific information in your memory about this, "
            f"simply answer: 'I don't have information about this in my database.' "
            f"Do not invent facts.\n"
            f"Question: {query}"
        )
    
    context_text = "\n---\n".join(context_chunks)
    
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
        response = ollama.generate(model='phi3:mini', prompt=prompt, stream=False)
        return response['response']
        
    except Exception as e:
        return f"Ошибка при вызове LLM: {e}. Убедись, что LLM запущена!"