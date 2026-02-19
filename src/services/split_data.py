from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_docs(prepared_docs, chunk_size=300, chunk_overlap=50):
    """
    Разбивает список текстов на чанки.
    
    Args:
        prepared_docs (list[str]): Список строк (текстов).
        chunk_size (int): Размер одного чанка в символах.
        chunk_overlap (int): Сколько символов захватывать из предыдущего чанка (контекст).
    """
    

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = splitter.create_documents(prepared_docs)
    print(f"✅ Разбиение завершено. Исходных доков: {len(prepared_docs)}, создано чанков: {len(chunks)}")
    return chunks