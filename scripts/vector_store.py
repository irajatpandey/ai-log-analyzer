import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
from sentence_transformers import SentenceTransformer
import chromadb
import json, os, shutil, re

# Configuration
from pathlib import Path
# Current script directory se relative path banao
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DATA_PATH = BASE_DIR / "logs" / "logs" / "processed_logs.json"
DB_PATH = BASE_DIR / "data" / "vector_db"


def clean_log(log_text):
    """Log se kachra (Date/IP) hatane ke liye"""
    log_text = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', '', log_text)
    log_text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '', log_text)
    return log_text.strip().lower()


knowledge_map = {
    "SSL": "SSL certificate expired. Fix: Renew via Certbot.",
    "password": "Credential expired. Fix: Rotate password in Vault.",
    "Connection refused": "Service Down. Fix: Check if target service is running."
}


def get_suggested_fix(log_text):
    for key, fix in knowledge_map.items():
        if key.lower() in log_text.lower():
            return fix
    return "Unknown Issue. Fix: Manual check needed."


# Fresh start
if os.path.exists(DB_PATH):
    shutil.rmtree(DB_PATH)

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.create_collection(name="app_logs", metadata={"hnsw:space": "cosine"})


def refresh_db():
    with open(LOG_DATA_PATH, 'r') as f:
        logs = json.load(f)

    print("Refreshing Clean Database...")
    for i, entry in enumerate(logs):
        # YAHAN CLEANING HO RAHI HAI
        cleaned_text = clean_log(entry['raw_log'])
        embedding = model.encode(cleaned_text, normalize_embeddings=True).tolist()
        fix = get_suggested_fix(cleaned_text)

        collection.add(
            embeddings=[embedding],
            documents=[cleaned_text],
            metadatas=[{"suggested_fix": fix}],
            ids=[f"log_{i}"]
        )
    print("Database Cleaned and Refreshed!")


if __name__ == "__main__":
    refresh_db()