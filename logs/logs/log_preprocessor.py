import re
import os
import json
from datetime import datetime

# Path definition
LOG_FILE_PATH = "./app.log"
OUTPUT_FILE_PATH = "./processed_logs.json"


def tokenize_log(line):
    clean_line = re.sub(r'[^\w\s]', ' ', line)
    tokens = clean_line.lower().split()
    return tokens


def process_and_save_logs():
    if not os.path.exists(LOG_FILE_PATH):
        print(f"File not found: {LOG_FILE_PATH}")
        return

    processed_data = []

    with open(LOG_FILE_PATH, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                tokens = tokenize_log(line)
                log_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "raw_log": line,
                    "tokens": tokens,
                    "token_count": len(tokens)
                }
                processed_data.append(log_entry)

    # Ab is list ko JSON file mein save karte hain
    with open(OUTPUT_FILE_PATH, 'w') as f:
        json.dump(processed_data, f, indent=4)

    print(f"Done! {len(processed_data)} logs process ho kar '{OUTPUT_FILE_PATH}' mein save ho gaye hain.")


if __name__ == "__main__":
    process_and_save_logs()