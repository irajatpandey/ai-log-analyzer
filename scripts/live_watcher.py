import time
import os
import warnings
import re
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
from get_solution import get_solution

warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

# --- Configuration (Exactly as your old working code) ---
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
LOG_FILE_PATH = PROJECT_DIR / "logs" / "app.log"
DB_PATH = PROJECT_DIR / "data" / "vector_db"
THRESHOLD = 0.80

# --- Rate Limit Config (Triple Checked for Free Key) --- [cite: 2025-10-01]
LAST_AI_CALL_TIME = 0
AI_COOLDOWN = 4.5  # 15 RPM ke liye safe gap

# --- Initialize ---
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path=str(DB_PATH))
collection = client.get_or_create_collection(name="app_logs")


def clean_log(log_text):
    """Timestamp aur IPs hata kar log saaf karta hai"""
    log_text = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', '', log_text)
    log_text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '', log_text)
    return log_text.strip().lower()


def process_new_line(line):
    global LAST_AI_CALL_TIME
    """Har nayi line ka solution dhoondhta hai with throttling safety"""
    if any(keyword in line for keyword in ["ERROR", "FATAL", "CRITICAL"]):
        sanitized = clean_log(line)
        query_vector = model.encode(sanitized, normalize_embeddings=True).tolist()
        results = collection.query(query_embeddings=[query_vector], n_results=1)

        if results['documents'] and results['distances']:
            match_percentage = 1 - results['distances'][0][0]

            if match_percentage >= THRESHOLD:
                solution = results['metadatas'][0][0].get('suggested_fix', "Manual check needed.")
                print(f"\n🚨 [SENTINEL ALERT] Match: {round(match_percentage * 100, 2)}%")
                print(f"Original: {line.strip()}")
                print(f"✅ Suggested Fix: {solution}")
            else:
                # --- Rate Limit Safety Logic ---
                now = time.time()
                elapsed = now - LAST_AI_CALL_TIME
                if elapsed < AI_COOLDOWN:
                    wait_needed = AI_COOLDOWN - elapsed
                    print(f"⏳ Rate Limit protection: Waiting {round(wait_needed, 1)}s...")
                    time.sleep(wait_needed)

                print(f"\n⚠️ [UNKNOWN ERROR] Match: {round(match_percentage * 100, 2)}%")
                print(f"Line: {line.strip()}")
                print("🤖 Gemini se solution dhundh raha hai...")

                llm_result = get_solution(sanitized, llm_provider="gemini")
                LAST_AI_CALL_TIME = time.time()  # Update timer after AI call

                print(f"Source: {llm_result.get('source')}")
                print(f"💡 AI Solution: {llm_result.get('solution')}")


def watch_logs():
    """Live file monitoring logic"""
    print(f"👀 AIOps Sentinel is watching: {LOG_FILE_PATH}...")  # Verified Path

    LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE_PATH.exists():
        LOG_FILE_PATH.touch()

    with open(LOG_FILE_PATH, 'r') as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            process_new_line(line)


if __name__ == "__main__":
    watch_logs()