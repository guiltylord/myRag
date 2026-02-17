from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_docs(documents, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = splitter.create_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    return chunks
