def split_docs(prepared_docs, chunk_size=500, chunk_overlap=100):
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = splitter.create_documents(prepared_docs)
    print(f"Total chunks created: {len(chunks)}")
    return chunks
