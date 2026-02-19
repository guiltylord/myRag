import sys
import colorama
from colorama import Fore, Style

from repositories.db_worker import connect_to_db, fetch_all_embeddings, close_db
from services.vectorize_data import embed_text
from services.retriever import get_scored_results, apply_threshold
from services.llm_service import build_prompt, call_llm 

colorama.init(autoreset=True)

THRESHOLD = 0.45
TOP_K = 2
PRINT_SCORES = True

def main():
    print(Fore.CYAN + "🚀 Инициализация RAG системы...")

    conn, cursor = connect_to_db()
    
    print(Fore.YELLOW + "📥 Прогрев модели эмбеддингов (подождите)...")
    embed_text("warmup") 

    db_rows = fetch_all_embeddings(cursor)
    
    if not db_rows:
        print(Fore.RED + "⚠ База данных пуста!")
    else:
        print(Fore.GREEN + f"✅ Система готова! В базе: {len(db_rows)} векторов.")
    
    print("---------------------------------------------------------")
    print(f"Параметры: THRESHOLD={THRESHOLD}, TOP_K={TOP_K}")
    print("Напиши свой вопрос. Для выхода напиши 'exit'.")

    while True:
        try:
            print("\n" + Fore.BLUE + "Твой вопрос: ", end="")
            user_query = input()

            if user_query.lower() in ['exit', 'quit', 'выход']:
                break
            
            if not user_query.strip():
                continue

            query_vector = embed_text(user_query)
            all_scores = get_scored_results(query_vector, db_rows)
            
            if PRINT_SCORES and all_scores:
                top_score = all_scores[0]['score']
                print(Fore.LIGHTBLACK_EX + f"[DEBUG] Top-1 Similarity: {top_score:.4f}")

            best_chunks = apply_threshold(all_scores, threshold=THRESHOLD, top_k=TOP_K)

            if best_chunks:
                print(Fore.CYAN + f"🔎 Найдено {len(best_chunks)} релевантных отрывков.")
            else:
                print(Fore.RED + "⚠ В базе нет точных совпадений. Отвечаю общими знаниями...")

            final_prompt = build_prompt(user_query, best_chunks)
            
            print(Fore.YELLOW + "🤖 Phi-3 генерирует ответ...")
            answer = call_llm(final_prompt)

            print(Fore.GREEN + "Ответ:")
            print(answer)
            print("-" * 30)

        except KeyboardInterrupt:
            print("\nВыход...")
            break
        except Exception as e:
            print(Fore.RED + f"❌ Произошла ошибка: {e}")

    close_db(conn, cursor)
    print(Fore.MAGENTA + "Пока!")

if __name__ == "__main__":
    main()