# AI-Based Intrusion Detection System (IDS) for IoT CCTV Access Monitoring

This repository is a student-ready mini-project that detects and notifies the owner when an unknown client accesses an IP CCTV camera on the local network. It combines a lightweight rule-based network monitor (real-time alerts) with an optional AI-based anomaly detector (IsolationForest) trained on collected access logs.

## Contents
See the repository layout:
```
AI-Based-IDS-for-IoT-CCTV/
├── src/
│   ├── camera_access_monitor.py
│   ├── ai_anomaly_detector.py
│   └── utils.py
├── data/
│   ├── logs.csv
│   └── trained_model.joblib  (placeholder)
├── docs/
│   ├── project_report.md
│   └── architecture_diagram.png
├── requirements.txt
├── README.md
└── LICENSE
```

## Quick start (Raspberry Pi / Linux)
1. Install Python 3.8+ and pip.
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Set Telegram credentials (either export or edit `src/utils.py`):
   ```bash
   export TELEGRAM_BOT_TOKEN="your_bot_token"
   export TELEGRAM_CHAT_ID="your_chat_id"
   ```
4. Update `src/camera_access_monitor.py` with your camera IPs or edit the `CAMERA_IPS` mapping.
5. Run the monitor (requires root for packet sniffing):
   ```bash
   sudo python3 src/camera_access_monitor.py
   ```

## Notes for demo
- Access your CCTV feed from another device (phone hotspot works). If the source IP is not in the allowed prefixes, you'll receive a Telegram alert.
- After collecting logs in `data/logs.csv`, run the AI module:
   ```bash
   python3 src/ai_anomaly_detector.py --train
   python3 src/ai_anomaly_detector.py --detect --src data/logs.csv
   ```
- The AI module uses IsolationForest to mark unusual sessions. Model saved to `data/trained_model.joblib`.

## Student deliverables included
- Working scripts
- Example logs
- Mini project report template and block-diagram
- Requirements.txt for easy install