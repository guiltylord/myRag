from db_worker import close_db, connect_to_db
from prepare_data import prepare_docs
from save_vectors import save_vectors
from split_data import split_docs
from vectorize_data import create_vectors_data

prepared_docs = prepare_docs()
chunks = split_docs(prepared_docs)
vectors = create_vectors_data(chunks)

connection, db_cursor = connect_to_db()

save_vectors(connection, db_cursor, vectors)
print(close_db)
