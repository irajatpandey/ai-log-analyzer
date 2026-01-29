from flask import Flask
import re
import json
app = Flask(__name__)

# @app.route("/get-logs")
def load_logs_from_service():
    pattern = re.compile(r"error", re.IGNORECASE)
    with open("java_logs.txt", "r") as file:
        for line in file:
            if pattern.search(line):
                print(line.strip())


def parse_mixed_logs():
    pattern = re.compile(r"(ERROR|FATAL|CRITICAL|\[error\]|\[crit\])(?:[:\s]|in\sapp:)+(.*)", re.IGNORECASE)

    print("📂 Reading logs from file...\n" + "-" * 50)

    try:
        # FILE READING START HERE
        with open("java_logs.txt", "r") as file:

            for line in file:
                line = line.strip()
                if not line: continue  # Empty line skip karo

                # --- 1. JSON Check ---
                if line.startswith('{'):
                    try:
                        data = json.loads(line)
                        if data.get('level') in ['error', 'critical', 'fatal']:
                            print(f"🚨 [JSON ERROR] Service: {data.get('service')} -> {data.get('msg')}")
                    except:
                        continue

                        # --- 2. Python Exception Check (Traceback) ---
                # Agar line mein koi specific Exception class dikhe
                elif "Exception" in line or "Error:" in line:
                    print(f"🔥 [TRACEBACK] {line}")

                # --- 3. Text Log Regex Check ---
                else:
                    match = pattern.search(line)
                    if match:
                        # Group 2 mein asli message hai
                        clean_msg = match.group(2).strip()
                        print(f"⚠️ [TEXT ERROR] {clean_msg}")

    except FileNotFoundError:
        print("❌ Error: 'server_logs.txt' file nahi mili. Please file create karein.")

    print("-" * 50 + "\n✅ Parsing Complete")

# Run function
parse_mixed_logs()

# load_logs_from_service()





