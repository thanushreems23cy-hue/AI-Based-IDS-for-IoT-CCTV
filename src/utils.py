import os
import csv
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')
DEFAULT_CONFIG = {
    "CAMERA_IPS": {"192.168.1.10": "FrontDoorCam"},
    "ALLOWED_REMOTE_PREFIXES": ["192.168.", "10.0.", "172.16."],
    "ALERT_COOLDOWN": 120,
    "LOGFILE": os.path.join("data", "logs.csv")
}

def load_config():
    # Attempt to read config.json in repo root; otherwise use defaults
    try:
        path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        if os.path.exists(path):
            with open(path, 'r') as f:
                cfg = json.load(f)
                return cfg
    except Exception:
        pass
    return DEFAULT_CONFIG

def send_telegram(message: str):
    import os, requests
    bot = os.getenv('TELEGRAM_BOT_TOKEN')
    chat = os.getenv('TELEGRAM_CHAT_ID')
    if not bot or not chat:
        print('[!] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set. Skipping send.')
        return
    url = f'https://api.telegram.org/bot{bot}/sendMessage'
    payload = {'chat_id': chat, 'text': message}
    try:
        r = requests.post(url, json=payload, timeout=5)
        if r.status_code != 200:
            print('[!] Telegram error:', r.status_code, r.text)
    except Exception as e:
        print('[!] Exception sending telegram:', e)

def append_log(logfile, record: dict):
    header = ['timestamp','camera_ip','camera_name','source_ip','allowed']
    first = not os.path.exists(logfile)
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    with open(logfile, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if first:
            writer.writeheader()
        writer.writerow(record)

def is_allowed_remote(ip: str, prefixes=None):
    if prefixes is None:
        prefixes = DEFAULT_CONFIG['ALLOWED_REMOTE_PREFIXES']
    for p in prefixes:
        if ip.startswith(p):
            return True
    return False
