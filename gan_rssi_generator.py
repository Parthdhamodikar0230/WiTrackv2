# calibrate_and_generate.py
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class WiFiPathLossModel:
    def __init__(self):
        self.P0 = -30  # Reference power at 1m (dBm)
        self.n = 2.0   # Path loss exponent
        self.sigma = 4 # Shadowing standard deviation
        
    def calibrate(self, distances, rssi_measurements):
        """Calibrate path loss model from real measurements"""
        # Linear regression: rssi = P0 - 10*n*log10(d)
        X = -10 * np.log10(np.array(distances)).reshape(-1,1)
        y = np.array(rssi_measurements)
        
        model = LinearRegression().fit(X, y)
        self.n = model.coef_[0]
        self.P0 = model.intercept_
        
        # Calculate R² for model quality
        r2 = model.score(X, y)
        print(f"Calibrated: P0={self.P0:.1f} dBm, n={self.n:.2f}, R²={r2:.3f}")
        return self
    
    def predict_rssi(self, distances, add_noise=True):
        """Predict RSSI for given distances"""
        distances = np.maximum(distances, 0.1)  # Avoid log(0)
        rssi = self.P0 - 10 * self.n * np.log10(distances)
        
        if add_noise:
            rssi += np.random.normal(0, self.sigma, len(distances))
        
        # Physical constraints: indoor WiFi typically -90 to -20 dBm
        return np.clip(rssi, -95, -15)
    
    def predict_distance(self, rssi):
        """Inverse: predict distance from RSSI"""
        rssi = np.clip(rssi, -95, -15)  # Avoid invalid values
        return 10 ** ((self.P0 - rssi) / (10 * self.n))

# Create realistic training data
def create_realistic_dataset(model, n_samples=5000):
    """Generate realistic RSSI-distance pairs"""
    
    # Multi-modal distance distribution (more samples at common distances)
    distances = np.concatenate([
        np.random.exponential(2, n_samples//3) + 0.5,      # Close devices
        np.random.normal(8, 3, n_samples//3),              # Medium range
        np.random.uniform(15, 25, n_samples//3)            # Far devices
    ])
    distances = np.clip(distances, 0.5, 30)
    
    # Generate corresponding RSSI with realistic noise
    rssi_values = model.predict_rssi(distances, add_noise=True)
    
    return pd.DataFrame({
        'distance_m': distances,
        'rssi': rssi_values
    })

if __name__ == "__main__":
    # Example calibration data (replace with your measurements)
    cal_distances = [1, 2, 3, 5, 8, 12, 20]
    cal_rssi = [-35, -42, -48, -55, -65, -72, -80]
    
    # Calibrate model
    model = WiFiPathLossModel().calibrate(cal_distances, cal_rssi)
    
    # Generate realistic dataset
    dataset = create_realistic_dataset(model, 10000)
    dataset.to_csv('realistic_wifi_data.csv', index=False)
    
    # Visualize
    plt.figure(figsize=(10,6))
    plt.scatter(dataset['distance_m'], dataset['rssi'], alpha=0.3, s=1)
    plt.xlabel('Distance (m)')
    plt.ylabel('RSSI (dBm)')
    plt.title('Realistic WiFi RSSI vs Distance')
    plt.grid(True)
    plt.savefig('rssi_distance_plot.png')
    plt.show()
    
    print(f"Generated {len(dataset)} realistic samples")
