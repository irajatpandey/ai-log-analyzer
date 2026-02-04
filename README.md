# 🛡️ AIOps Log Sentinel

> **An Intelligent, Event-Driven Log Monitoring System powered by RAG (Retrieval-Augmented Generation) and Google Gemini AI.**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![Database](https://img.shields.io/badge/Vector%20DB-ChromaDB-green)
![DevOps](https://img.shields.io/badge/DevOps-Self--Healing-purple)

## 📖 Overview

**AIOps Log Sentinel** is a next-generation monitoring tool designed to reduce Mean Time To Resolution (MTTR). Instead of just alerting you about an error, it **diagnoses** it and provides a **fix** in real-time.

It uses a **Hybrid RAG Architecture**:
1.  **Layer 1 (Speed):** Instantly searches a local **Vector Database (ChromaDB)** for known error patterns and historical fixes.
2.  **Layer 2 (Intelligence):** If the error is new, it consults **Google Gemini 1.5 Flash (AI)** to analyze the log and generate a DevOps-grade solution.

## 🚀 Key Features

* **⚡ Real-Time Monitoring:** Watches log streams live using a lightweight file watcher.
* **🧠 Vector Search (RAG):** Uses Semantic Search (Sentence Transformers) to find similar past incidents with >90% accuracy.
* **🤖 AI Fallback:** Automatically queries Google Gemini API for unknown/novel errors.
* **📉 Rate Limit Protection:** Smart throttling ensures you never hit API quota limits.
* **🔥 Chaos Engineering:** Includes a `chaos_logs.py` module to simulate real-world DevOps disasters (DB timeouts, SSL expiry, OOM kills) for testing.

---

## 🛠️ Project Structure

```bash
project/
├── data/
│   └── vector_db/       # ChromaDB persistent storage
├── logs/
│   ├── app.log          # The active log file being watched
│   └── chaos_logs.py    # Script to generate fake error logs
├── scripts/
│   ├── live_watcher.py  # Main Sentinel Engine (The "Brain")
│   ├── vector_store.py  # Initializes/Refreshes the Vector DB
│   └── get_solution.py  # Handles AI API connectivity (Google Gemini)
├── .env                 # API Keys (Not committed)
├── docker-compose.yml   # Container orchestration
└── requirements.txt     # Python dependencies
