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
    print(Fore.CYAN + "\n=== RAG SYSTEM INITIALIZATION ===")
    
    conn, cursor = connect_to_db()
    
    print(Fore.YELLOW + "[..] Warming up embedding model...")
    embed_text("warmup") 

    db_rows = fetch_all_embeddings(cursor)
    
    if not db_rows:
        print(Fore.RED + "[!!] Database is empty.")
    else:
        print(Fore.GREEN + f"[OK] System ready. Vectors loaded: {len(db_rows)}")
    
    print(Fore.CYAN + "------------------------------------------")
    print(f"Config: Threshold={THRESHOLD} | Top_K={TOP_K}")
    print("Type your question below. Type 'exit' to quit.")
    print(Fore.CYAN + "------------------------------------------")

    while True:
        try:
            print(Fore.BLUE + "\nUser Query > ", end="")
            user_query = input()

            if user_query.lower() in ['exit', 'quit', 'выход']:
                break
            
            if not user_query.strip():
                continue

            query_vector = embed_text(user_query)
            all_scores = get_scored_results(query_vector, db_rows)
            
            if PRINT_SCORES and all_scores:
                top_score = all_scores[0]['score']
                print(Fore.LIGHTBLACK_EX + f"     [DEBUG] Best Similarity Score: {top_score:.4f}")

            best_chunks = apply_threshold(all_scores, threshold=THRESHOLD, top_k=TOP_K)

            if best_chunks:
                print(Fore.CYAN + f"     [INFO] Found {len(best_chunks)} relevant context chunks.")
            else:
                print(Fore.RED + "     [WARN] No relevant context found. Using general knowledge.")

            final_prompt = build_prompt(user_query, best_chunks)
            
            print(Fore.YELLOW + "     [..] Phi-3 is generating response...")
            answer = call_llm(final_prompt)

            print(Fore.GREEN + "\nResponse:")
            print(answer)
            print(Fore.CYAN + "-" * 42)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(Fore.RED + f"\n[ERROR] {e}")

    close_db(conn, cursor)
    print(Fore.MAGENTA + "\nGoodbye!")

if __name__ == "__main__":
    main()