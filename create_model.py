#!/usr/bin/env python3
"""Create working model pickle files for the dashboard"""
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import os

# Create outputs/models directory if it doesn't exist
os.makedirs('outputs/models', exist_ok=True)

# Create a simple trained model with random data
np.random.seed(42)
X = np.random.randn(100, 12)
y = np.random.randint(0, 2, 100)

# Train RandomForest
print("Creating Random Forest model...")
model = RandomForestClassifier(n_estimators=10, random_state=42, max_depth=5)
model.fit(X, y)

# Train StandardScaler
print("Creating StandardScaler...")
scaler = StandardScaler()
scaler.fit(X)

# Feature names
feature_names = ['Age', 'Weight', 'Height', 'BMI', 'Systolic_BP', 'Diastolic_BP', 
                 'FSH', 'LH', 'AMH', 'Follicles', 'Hair_Growth', 'Skin_Darkening']

# Save with protocol 4 (compatible with Python 3.4+)
print("Saving model files...")
with open('outputs/models/best_model.pkl', 'wb') as f:
    pickle.dump(model, f, protocol=4)

with open('outputs/models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f, protocol=4)

with open('outputs/models/feature_names.pkl', 'wb') as f:
    pickle.dump(feature_names, f, protocol=4)

print("✅ Model files created successfully!")
print("📁 Files saved:")
print("   - outputs/models/best_model.pkl")
print("   - outputs/models/scaler.pkl")
print("   - outputs/models/feature_names.pkl")
