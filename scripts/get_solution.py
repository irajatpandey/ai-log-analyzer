import os
import requests
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
DB_PATH = Path(__file__).parent.parent / "data" / "vector_db"
MODEL_NAME = 'all-MiniLM-L6-v2'
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def get_llm_solution(error_log):
    """Direct stable V1 API call - No more v1beta/404 errors"""
    # Strictly using v1 (Stable) instead of v1beta
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
    headers = {'Content-Type': 'application/json'}

    payload = {
        "contents": [{
            "parts": [{
                "text": f"You are a Senior DevOps Engineer. Provide a concise, 2-line technical fix for: {error_log}"
            }]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        result = response.json()

        if response.status_code == 200:
            return {
                "solution": result['candidates'][0]['content']['parts'][0]['text'],
                "source": "google_gemini_v1_stable"
            }
        else:
            # Error details specifically for debugging
            return {"solution": f"Gemini Error: {result.get('error', {}).get('message')}", "source": "error"}

    except Exception as e:
        return {"solution": f"Request failed: {str(e)}", "source": "error"}


def get_solution(error_log: str, similarity_score: float = None, llm_provider: str = "gemini") -> dict:
    """Main Entry Point"""
    try:
        st_model = SentenceTransformer(MODEL_NAME)
        db_client = chromadb.PersistentClient(path=str(DB_PATH))
        collection = db_client.get_or_create_collection(name="app_logs")

        # 1. Vector Search
        embedding = st_model.encode(error_log).tolist()
        results = collection.query(query_embeddings=[embedding], n_results=1)

        # 2. Match Check
        if results['distances'] and results['distances'][0]:
            score = 1 - results['distances'][0][0]
            if score >= 0.8:
                return {
                    "solution": results['metadatas'][0][0].get('suggested_fix'),
                    "source": "vector_db",
                    "similarity": round(score, 2)
                }

        # 3. Fallback to Stable V1 API
        return get_llm_solution(error_log)

    except Exception as e:
        return {"solution": f"System Error: {str(e)}", "source": "error"}