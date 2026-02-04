import chromadb

# Path wahi jo aap use kar rahe hain
DB_PATH = "../data/vector_db"

client = chromadb.PersistentClient(path=DB_PATH)
try:
    collection = client.get_collection(name="app_logs")

    # Hum pehle 3 logs nikaal kar dekhenge
    results = collection.peek(limit=3)

    print("\n🔍 --- DATABASE INSPECTION --- 🔍")
    if not results['ids']:
        print("❌ Database empty hai! vector_store.py dobara run karein.")
    else:
        for i in range(len(results['ids'])):
            print(f"\n📄 Log ID: {results['ids'][i]}")
            # Ye wo exact text hai jo match hona chahiye
            print(f"📝 EXACT STORED TEXT: '{results['documents'][i]}'")
            print(f"💡 Metadata: {results['metadatas'][i]}")
            print("-" * 40)

except Exception as e:
    print(f"Error: {e}")
    print("Shayad collection ka naam galat hai ya DB path galat hai.")