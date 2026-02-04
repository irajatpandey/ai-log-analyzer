import chromadb
import pandas as pd

DB_PATH = "../data/vector_db"

def export_with_vectors():
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name="app_logs")

    results = collection.get(include=["documents", "metadatas", "embeddings"])

    data = []
    for i in range(len(results['ids'])):
        data.append({
            "ID": results['ids'][i],
            "Log_Message": results['documents'][i],

            "Vector_Sample": results['embeddings'][i][:5],
            "Timestamp": results['metadatas'][i].get('timestamp', 'N/A')
        })

    df = pd.DataFrame(data)
    df.to_csv("../data/db_vectors_check.csv", index=False)
    print("Bhai, ab CSV check karo, 'Vector_Sample' column mein numbers dikhenge!")

if __name__ == "__main__":
    export_with_vectors()