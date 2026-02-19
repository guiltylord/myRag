import sys
import colorama # Для красоты (pip install colorama), если нет - удали строки с Fore
from colorama import Fore, Style

# Импорты твоих сервисов
from repositories.db_worker import connect_to_db, fetch_all_embeddings, close_db
from services.vectorize_data import embed_text
from services.retriever import get_scored_results, apply_threshold
from services.llm_service import build_prompt, call_llm

# Инициализация цветов для консоли
colorama.init(autoreset=True)

def main():
    print(Fore.CYAN + "🚀 Инициализация RAG системы...")

    # 1. Подключаемся к базе и модели ОДИН РАЗ при запуске
    conn, cursor = connect_to_db()
    
    # Загружаем модель сразу, чтобы не ждать потом
    print(Fore.YELLOW + "📥 Загружаю модель эмбеддингов (подождите)...")

    # Выкачиваем базу в память (если база огромная, так делать не надо, но для теста ок)
    db_rows = fetch_all_embeddings(cursor)
    print(Fore.GREEN + f"✅ Система готова! В базе {len(db_rows)} документов.")
    print("---------------------------------------------------------")
    print("Напиши свой вопрос и нажми Enter. Для выхода напиши 'exit'.")

    # --- БЕСКОНЕЧНЫЙ ЦИКЛ ЧАТА ---
    while True:
        print("\n" + Fore.BLUE + "Твой вопрос: ", end="")
        user_query = input() # <--- ВОТ ТУТ МЫ ЖДЕМ ТВОЙ ВВОД

        # Проверка на выход
        if user_query.lower() in ['exit', 'quit', 'выход']:
            break
        
        if not user_query.strip():
            continue

        try:
            # 2. Векторизация
            # Используем embed_text (она сама возьмет закешированную модель)
            query_vector = embed_text(user_query)

            # 3. Поиск (Retriever)
            all_scores = get_scored_results(query_vector, db_rows)
            
            # Порог 0.4 - если меньше, считаем, что инфы нет
            best_chunks = apply_threshold(all_scores, threshold=0.4, top_k=2)

            if best_chunks:
                print(Fore.CYAN + f"🔎 Нашел {len(best_chunks)} отрывков в базе...")
            else:
                print(Fore.RED + "⚠ В базе нет ничего похожего. Отвечаю из общих знаний...")

            # 4. LLM
            final_prompt = build_prompt(user_query, best_chunks)
            
            print(Fore.YELLOW + "🤖 Phi-3 думает...")
            answer = call_llm(final_prompt)

            # Вывод ответа
            print(Fore.GREEN + "Ответ:")
            print(answer)
            print("-" * 30)

        except Exception as e:
            print(Fore.RED + f"Ошибка: {e}")

    # Закрытие при выходе из цикла
    close_db(conn, cursor)
    print("Пока!")

if __name__ == "__main__":
    main()