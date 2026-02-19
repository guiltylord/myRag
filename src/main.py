import colorama
from colorama import Fore

from repositories.db_worker import connect_to_db, fetch_all_embeddings, close_db
from services.vectorize_data import embed_text
from services.retriever import get_scored_results, apply_threshold
from services.llm_service import build_prompt, call_llm

colorama.init(autoreset=True)

def main():
    print(Fore.CYAN + "🚀 Инициализация RAG системы...")

    conn, cursor = connect_to_db()
    
    print(Fore.YELLOW + "📥 Загружаю модель эмбеддингов (подождите)...")

    db_rows = fetch_all_embeddings(cursor)
    print(Fore.GREEN + f"✅ Система готова! В базе {len(db_rows)} документов.")
    print("---------------------------------------------------------")
    print("Напиши свой вопрос и нажми Enter. Для выхода напиши 'exit'.")

    while True:
        print("\n" + Fore.BLUE + "Твой вопрос: ", end="")
        user_query = input()

        if user_query.lower() in ['exit', 'quit', 'выход']:
            break
        
        if not user_query.strip():
            continue

        try:
            query_vector = embed_text(user_query)

            all_scores = get_scored_results(query_vector, db_rows)
            
            best_chunks = apply_threshold(all_scores, threshold=0.4, top_k=2)

            if best_chunks:
                print(Fore.CYAN + f"🔎 Нашел {len(best_chunks)} отрывков в базе...")
            else:
                print(Fore.RED + "⚠ В базе нет ничего похожего. Отвечаю из общих знаний...")

            final_prompt = build_prompt(user_query, best_chunks)
            
            print(Fore.YELLOW + "🤖 Phi-3 думает...")
            answer = call_llm(final_prompt)

            print(Fore.GREEN + "Ответ:")
            print(answer)
            print("-" * 30)

        except Exception as e:
            print(Fore.RED + f"Ошибка: {e}")

    close_db(conn, cursor)
    print("Пока!")

if __name__ == "__main__":
    main()