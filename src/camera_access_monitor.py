#!/usr/bin/env python3
"""camera_access_monitor.py
Monitors TCP SYN packets towards configured camera IPs and sends a Telegram alert
if a new (unauthorized) source tries to access the camera. Logs events to CSV.
"""

import os
import time
import csv
import argparse
from datetime import datetime
from scapy.all import sniff, TCP, IP
from utils import send_telegram, append_log, is_allowed_remote, load_config

# Load configuration (CAMERA_IPS etc.)
cfg = load_config()

CAMERA_IPS = cfg.get("CAMERA_IPS", {"192.168.1.10": "FrontDoorCam"})
ALLOWED_REMOTE_PREFIXES = cfg.get("ALLOWED_REMOTE_PREFIXES", ["192.168.", "10.0.", "172.16."])
ALERT_COOLDOWN = cfg.get("ALERT_COOLDOWN", 120)
LOGFILE = cfg.get("LOGFILE", "data/logs.csv")

_last_alert = {}

def packet_handler(pkt):
    if TCP in pkt and IP in pkt:
        ip = pkt[IP]
        tcp = pkt[TCP]
        if tcp.flags & 0x02:  # SYN
            dst = ip.dst
            src = ip.src
            if dst in CAMERA_IPS:
                cam_name = CAMERA_IPS.get(dst, dst)
                key = f"{src}->{dst}"
                now = time.time()
                last = _last_alert.get(key, 0)
                if now - last < ALERT_COOLDOWN:
                    return
                _last_alert[key] = now

                allowed = is_allowed_remote(src, ALLOWED_REMOTE_PREFIXES)
                ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                msg = (f"🚨 CCTV Access Alert\n"
                       f"Camera: {cam_name} ({dst})\n"
                       f"Source IP: {src}\n"
                       f"Allowed?: {'Yes' if allowed else 'No'}\n"
                       f"Time: {ts}")
                print(msg)
                append_log(LOGFILE, {
                    'timestamp': ts,
                    'camera_ip': dst,
                    'camera_name': cam_name,
                    'source_ip': src,
                    'allowed': allowed
                })
                send_telegram(msg)

def main():
    print("Starting CCTV access monitor...")
    cams = " or ".join(f"dst host {ip}" for ip in CAMERA_IPS.keys())
    bpf_filter = f"tcp and ({cams})"
    sniff(filter=bpf_filter, prn=packet_handler, store=False)

if __name__ == '__main__':
    main()
