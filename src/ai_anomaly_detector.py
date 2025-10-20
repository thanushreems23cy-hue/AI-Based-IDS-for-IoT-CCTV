#!/usr/bin/env python3
"""ai_anomaly_detector.py

Simple IsolationForest-based anomaly detection on logs produced by camera_access_monitor.py
Usage:
    python ai_anomaly_detector.py --train --src data/logs.csv
    python ai_anomaly_detector.py --detect --src data/logs.csv
"""

import argparse
import os

def train(src='data/logs.csv', model_out='data/trained_model.joblib'):
    try:
        import pandas as pd
        from sklearn.ensemble import IsolationForest
        from sklearn.preprocessing import StandardScaler
        import joblib
    except Exception as e:
        print('Missing ML packages. Install requirements.txt to enable training.')
        return

    if not os.path.exists(src):
        print(f'Log file "{src}" not found. Generate logs first by running the monitor.')
        return

    df = pd.read_csv(src, parse_dates=['timestamp'])
    # Basic feature engineering
    df['hour'] = df['timestamp'].dt.hour
    df['is_allowed'] = df['allowed'].astype(int)
    features = ['hour','is_allowed']
    X = df[features].fillna(0)

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    clf = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
    clf.fit(Xs)

    joblib.dump({'model': clf, 'scaler': scaler, 'features': features}, model_out)
    print('Model trained and saved to', model_out)

def detect(src='data/logs.csv', model_in='data/trained_model.joblib'):
    try:
        import pandas as pd
        import joblib
    except Exception:
        print('Missing packages. Install requirements.txt to run detection.')
        return

    if not os.path.exists(model_in):
        print('Model file not found. Run with --train first.')
        return
    if not os.path.exists(src):
        print('Log file not found.')
        return

    obj = joblib.load(model_in)
    clf = obj['model']; scaler = obj['scaler']; features = obj['features']
    df = pd.read_csv(src, parse_dates=['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['is_allowed'] = df['allowed'].astype(int)
    X = df[features].fillna(0)
    Xs = scaler.transform(X)
    preds = clf.predict(Xs)  # -1 anomaly, 1 normal
    df['anomaly'] = (preds == -1)
    print(df[['timestamp','camera_name','source_ip','allowed','anomaly']].tail(20))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', action='store_true')
    parser.add_argument('--detect', action='store_true')
    parser.add_argument('--src', default='data/logs.csv')
    args = parser.parse_args()
    if args.train:
        train(src=args.src)
    if args.detect:
        detect(src=args.src)
