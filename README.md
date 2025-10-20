# AI-Based-IDS-for-IoT-CCTV
# AI-Based Intrusion Detection System for IoT CCTV

This repository presents a **Python-based AI Intrusion Detection System (IDS)** designed for **IoT-enabled CCTV devices**.  
The system detects **unauthorized access attempts** and provides **real-time alerts**, ensuring network and video surveillance security.

---

## 🚀 Features
- Detects **unauthorized CCTV access** using AI.
- Supports **Raspberry Pi** deployment for edge monitoring.
- Utilizes **Deep Learning / ML** models for intrusion classification.
- Includes notification alert mechanism.
- Lightweight implementation for IoT environments.

---

## 🧠 Tech Stack
- **Language:** Python 3.x  
- **Libraries:** TensorFlow / PyTorch, scikit-learn, OpenCV, pandas, numpy  
- **Hardware:** Raspberry Pi (optional)  
- **Interface:** Flask dashboard or console alerts  

---

## 🧩 Folder Overview
| Folder | Purpose |
|--------|----------|
| `src/` | Core code (intrusion detection, utilities) |
| `scripts/` | Training & inference scripts |
| `models/` | Trained model files |
| `data/` | Datasets, logs |
| `docs/` | Documentation and diagrams |
| `original_files/` | Your original unmodified project files |

---

## ⚙️ Installation
```bash
git clone https://github.com/thanushreems23cy-hue/AI-Based-IDS-for-IoT-CCTV.git
cd AI-Based-IDS-for-IoT-CCTV
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
