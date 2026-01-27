# 🚀 AIOps Log Sentinel

### *Enterprise-Grade Observability Pipeline with Resilience & AI-Readiness*

**AIOps Log Sentinel** is a high-performance log processing pipeline designed to handle massive log volumes from distributed microservices. It ensures **zero data loss** during infrastructure failures (like Kafka downtime or Node scale-downs) by implementing a robust Disk Buffering strategy.

[Image of Log Pipeline: App Pods with Fluent Bit DaemonSet -> PVC Buffer -> Kafka -> Python AI Consumer]

---

## 🏗 System Architecture

The project follows a "Store-and-Forward" architecture to balance performance and reliability:

1. **Log Ingestion:** Fluent Bit tails logs from multiple sources (Java, Python, React).
2. **Reliable Buffering:** Implements **Filesystem Buffering** using PVC/EBS. Chunks are committed to disk before network transmission.
3. **Event Streaming:** Apache Kafka acts as the backbone, utilizing **Key-based Partitioning** to maintain strict log ordering per service.
4. **Intelligent Processing:** A Flask-based Python worker consumes streams, applies **Regex-based parsing**, and prepares data for AIOps analysis.

---

## 🛠 Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Shipper** | Fluent Bit | Log collection & Disk Buffering |
| **Stream** | Apache Kafka | Real-time event streaming |
| **Backend** | Python (Flask) | Log Parsing, Regex Engine & API |
| **Storage** | PVC / Local Disk | Persistence Layer (The "Safe Box") |
| **Container** | Docker Compose | Local Orchestration |

---

## 📂 Project Structure

- **app/**: Main application package.
  - **processor/**: Contains the Regex Engine for log structuring.
  - **services/**: Background threads for Kafka consumption.
  - **routes.py**: Flask API endpoints for status and alerts.
- **config/**: Infrastructure configurations (Fluent Bit & Environment).
- **logs/**: Mock application logs used for pipeline testing.
- **buffer/**: The "Safe Box" where Fluent Bit stores data chunks (EBS Simulation).
- **run.py**: The entry point to start the Flask sentinel.
