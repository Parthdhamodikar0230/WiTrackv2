# realtime_server_v2.py
import socket, json, joblib, threading, time
import pandas as pd, numpy as np
from collections import defaultdict, deque
from flask import Flask, jsonify, render_template

class AccurateDistanceEstimator:
    def __init__(self):
        self.model = joblib.load('wifi_distance_model_v2.pkl')
        self.scaler = joblib.load('wifi_scaler_v2.pkl')
        
        # Larger buffers for better accuracy
        self.rssi_buffers = defaultdict(lambda: deque(maxlen=20))
        self.device_data = {}
        
    def engineer_features(self, rssi_list):
        """Create features from RSSI buffer (same as training)"""
        df = pd.DataFrame({'rssi': rssi_list})
        
        features = {}
        for w in [3, 5, 10]:
            features[f'rssi_mean_{w}'] = df['rssi'].rolling(w, min_periods=1).mean().iloc[-1]
            features[f'rssi_std_{w}'] = df['rssi'].rolling(w, min_periods=1).std().fillna(0).iloc[-1]
            features[f'rssi_var_{w}'] = df['rssi'].rolling(w, min_periods=1).var().fillna(0).iloc[-1]
            features[f'rssi_min_{w}'] = df['rssi'].rolling(w, min_periods=1).min().iloc[-1]
            features[f'rssi_max_{w}'] = df['rssi'].rolling(w, min_periods=1).max().iloc[-1]
            features[f'rssi_range_{w}'] = features[f'rssi_max_{w}'] - features[f'rssi_min_{w}']
            
            if len(rssi_list) >= w:
                trend = np.polyfit(range(w), rssi_list[-w:], 1)[0]
            else:
                trend = 0
            features[f'rssi_trend_{w}'] = trend
        
        features['rssi_current'] = rssi_list[-1]
        
        return pd.DataFrame([features])
    
    def estimate_distance(self, bssid, rssi):
        """Estimate distance with confidence interval"""
        self.rssi_buffers[bssid].append(rssi)
        
        if len(self.rssi_buffers[bssid]) < 3:
            return None
        
        # Create features
        rssi_list = list(self.rssi_buffers[bssid])
        features = self.engineer_features(rssi_list)
        
        # Predict
        X_scaled = self.scaler.transform(features)
        distance = self.model.predict(X_scaled)[0]
        distance = max(0.1, min(50, distance))  # Reasonable bounds
        
        # Simple confidence based on signal stability
        rssi_std = np.std(rssi_list[-5:]) if len(rssi_list) >= 5 else 10
        confidence = max(0.1, min(1.0, 1.0 - (rssi_std / 10)))
        
        return {
            'distance': round(distance, 2),
            'confidence': round(confidence, 2),
            'rssi_avg': round(np.mean(rssi_list[-5:]), 1),
            'samples': len(rssi_list)
        }
    
    def process_scan(self, scan_data):
        """Process ESP8266 scan data"""
        results = []
        current_time = time.time()
        
        for device in scan_data.get('devices', []):
            bssid = device['bssid']
            rssi = device['rssi']
            
            result = self.estimate_distance(bssid, rssi)
            if result:
                result['bssid'] = bssid
                result['timestamp'] = current_time
                self.device_data[bssid] = result
                results.append(result)
        
        return results
    
    def get_active_devices(self, max_age=30):
        """Get devices seen within max_age seconds"""
        current_time = time.time()
        active = {}
        
        for bssid, data in self.device_data.items():
            if current_time - data['timestamp'] <= max_age:
                active[bssid] = data
        
        return active

# Flask web interface
app = Flask(__name__)
estimator = AccurateDistanceEstimator()

@app.route('/')
def dashboard():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Accurate WiFi Distance Tracker</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .device { margin: 10px; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }
        .distance { font-size: 1.3em; font-weight: bold; color: #2c5aa0; }
        .confidence { color: #666; }
        .high-conf { color: #28a745; }
        .med-conf { color: #ffc107; }
        .low-conf { color: #dc3545; }
        #status { margin: 20px 0; padding: 10px; background: #f8f9fa; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🔍 Accurate WiFi Distance Tracker</h1>
    <div id="status">Last update: --</div>
    <div id="devices"></div>
    
    <script>
        function getConfidenceClass(conf) {
            if (conf >= 0.7) return 'high-conf';
            if (conf >= 0.4) return 'med-conf';
            return 'low-conf';
        }
        
        async function updateDevices() {
            try {
                const res = await fetch('/api/devices');
                const devices = await res.json();
                const container = document.getElementById('devices');
                
                document.getElementById('status').innerHTML = 
                    `Last update: ${new Date().toLocaleTimeString()} | Active devices: ${Object.keys(devices).length}`;
                
                container.innerHTML = '';
                
                for (const [bssid, data] of Object.entries(devices)) {
                    const div = document.createElement('div');
                    div.className = 'device';
                    
                    const confClass = getConfidenceClass(data.confidence);
                    
                    div.innerHTML = `
                        <h3>📱 ${bssid}</h3>
                        <div class="distance">📏 Distance: ${data.distance} m</div>
                        <div class="confidence ${confClass}">🎯 Confidence: ${Math.round(data.confidence*100)}%</div>
                        <div>📶 RSSI: ${data.rssi_avg} dBm (${data.samples} samples)</div>
                        <div>🕐 Last seen: ${new Date(data.timestamp*1000).toLocaleTimeString()}</div>
                    `;
                    container.appendChild(div);
                }
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('status').innerHTML = 'Error fetching data';
            }
        }
        
        setInterval(updateDevices, 2000);
        updateDevices();
    </script>
</body>
</html>
    '''

@app.route('/api/devices')
def api_devices():
    return jsonify(estimator.get_active_devices())

def udp_server():
    """UDP server for ESP8266 data"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 4210))
    print("🚀 UDP server listening on port 4210")
    
    while True:
        try:
            data, addr = sock.recvfrom(2048)
            scan_data = json.loads(data.decode())
            
            results = estimator.process_scan(scan_data)
            
            if results:
                print(f"\n📡 Scan from {addr[0]}:")
                for r in results:
                    conf_icon = "🟢" if r['confidence'] > 0.7 else "🟡" if r['confidence'] > 0.4 else "🔴"
                    print(f"  {conf_icon} {r['bssid'][:17]}: {r['distance']}m (conf: {r['confidence']:.1f})")
                    
        except Exception as e:
            print(f"❌ UDP Error: {e}")

if __name__ == "__main__":
    # Start UDP server in background
    udp_thread = threading.Thread(target=udp_server, daemon=True)
    udp_thread.start()
    
    print("🌐 Web dashboard: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
