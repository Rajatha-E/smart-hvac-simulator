import pandas as pd

def detect_hvac_anomalies(log_file="hvac_telemetry_log.csv"):
    try:
        df = pd.read_csv(log_file)
    except FileNotFoundError:
        print("Log file not found. Run simulation.py first.")
        return
    
    anomalies = []
    print("Running Anomaly Detection Scan...")
    
    for i in range(1, len(df)):
        # Rule: If compressor is working hard but temperature is rising or stuck
        if df.loc[i, 'Temp'] >= df.loc[i-1, 'Temp'] and df.loc[i, 'Compressor'] == 'HIGH':
            anomalies.append(f"⚠️ Warning: Cycle {df.loc[i, 'Cycle']} - Temperature did not drop despite HIGH compressor output.")
            
    if anomalies:
        for a in anomalies:
            print(a)
    else:
        print("✅ No system anomalies detected. Normal operation.")

if __name__ == "__main__":
    detect_hvac_anomalies()