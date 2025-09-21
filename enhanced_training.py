# enhanced_training_v2.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

class AdvancedRSSIProcessor:
    def __init__(self):
        self.scaler = RobustScaler()  # More robust to outliers
        self.model = None
        
    def engineer_features(self, df, window_sizes=[3, 5, 10]):
        """Create advanced features from RSSI time series"""
        df = df.sort_index().copy()  # Maintain time order
        
        features = {}
        
        for w in window_sizes:
            # Basic statistics
            features[f'rssi_mean_{w}'] = df['rssi'].rolling(w, min_periods=1).mean()
            features[f'rssi_std_{w}'] = df['rssi'].rolling(w, min_periods=1).std().fillna(0)
            features[f'rssi_var_{w}'] = df['rssi'].rolling(w, min_periods=1).var().fillna(0)
            features[f'rssi_min_{w}'] = df['rssi'].rolling(w, min_periods=1).min()
            features[f'rssi_max_{w}'] = df['rssi'].rolling(w, min_periods=1).max()
            features[f'rssi_range_{w}'] = features[f'rssi_max_{w}'] - features[f'rssi_min_{w}']
            
            # Signal stability
            features[f'rssi_trend_{w}'] = df['rssi'].rolling(w, min_periods=2).apply(
                lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0
            )
        
        # Current signal strength (most important)
        features['rssi_current'] = df['rssi']
        
        # Convert to DataFrame
        feature_df = pd.DataFrame(features, index=df.index)
        return feature_df.fillna(method='bfill').fillna(0)
    
    def train(self, data_path='realistic_wifi_data.csv'):
        """Train the model with advanced features"""
        
        # Load data
        df = pd.read_csv(data_path)
        print(f"Loaded {len(df)} samples")
        
        # Create features
        features = self.engineer_features(df)
        target = df['distance_m']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=0.2, random_state=42, shuffle=False
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Try multiple models
        models = {
            'RandomForest': RandomForestRegressor(
                n_estimators=200, max_depth=15, random_state=42, n_jobs=-1
            ),
            'GradientBoosting': GradientBoostingRegressor(
                n_estimators=200, max_depth=8, learning_rate=0.1, random_state=42
            )
        }
        
        best_model = None
        best_score = float('inf')
        
        for name, model in models.items():
            # Cross-validation
            scores = cross_val_score(model, X_train_scaled, y_train, 
                                   cv=5, scoring='neg_mean_absolute_error')
            cv_mae = -scores.mean()
            
            # Train and test
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            test_mae = mean_absolute_error(y_test, y_pred)
            test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            
            print(f"{name}:")
            print(f"  CV MAE: {cv_mae:.2f} m")
            print(f"  Test MAE: {test_mae:.2f} m")
            print(f"  Test RMSE: {test_rmse:.2f} m")
            
            if test_mae < best_score:
                best_score = test_mae
                best_model = model
                self.model = model
        
        # Feature importance
        if hasattr(best_model, 'feature_importances_'):
            importance = pd.DataFrame({
                'feature': features.columns,
                'importance': best_model.feature_importances_
            }).sort_values('importance', ascending=False)
            print("\nTop 10 Most Important Features:")
            print(importance.head(10))
        
        # Save model
        self.save_model()
        return best_score
    
    def predict(self, rssi_buffer):
        """Predict distance from RSSI buffer"""
        # Create temporary DataFrame for feature engineering
        temp_df = pd.DataFrame({'rssi': rssi_buffer})
        features = self.engineer_features(temp_df)
        
        # Use only the last row (most recent)
        X = features.iloc[[-1]]
        X_scaled = self.scaler.transform(X)
        
        distance = self.model.predict(X_scaled)[0]
        return max(0.1, distance)  # Ensure positive
    
    def save_model(self):
        """Save trained model and scaler"""
        joblib.dump(self.model, 'wifi_distance_model_v2.pkl')
        joblib.dump(self.scaler, 'wifi_scaler_v2.pkl')
        print("Model saved as wifi_distance_model_v2.pkl")

if __name__ == "__main__":
    processor = AdvancedRSSIProcessor()
    mae = processor.train('realistic_wifi_data.csv')
    print(f"\nFinal model MAE: {mae:.2f} m")
