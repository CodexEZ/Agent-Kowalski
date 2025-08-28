
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import time
import json # Import json to parse the input data

# --- Logging setup ---
def log_message(message):
    print(f"[LOG] {message}")

# --- 1. Define the Neural Network Model ---
class DiabetesClassifier(nn.Module):
    def __init__(self, input_size):
        super(DiabetesClassifier, self).__init__()
        # Two hidden layers
        self.fc1 = nn.Linear(input_size, 64)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(64, 32)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(32, 1) # Output layer for binary classification

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu1(out)
        out = self.fc2(out)
        out = self.relu2(out)
        out = self.fc3(out)
        return out

# --- Data Loading and Preprocessing ---
def preprocess_data(raw_records_json):
    log_message("Starting data preprocessing...")
    records = json.loads(raw_records_json)

    if not records:
        raise ValueError("No records provided for preprocessing.")

    # Extract features and labels
    features = []
    labels = []
    feature_names = [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
    ]

    for record in records:
        current_features = [record[name] for name in feature_names]
        features.append(current_features)
        labels.append(record['Outcome'])

    X = np.array(features, dtype=np.float32)
    y = np.array(labels, dtype=np.float32).reshape(-1, 1)

    # Handle '0' values in specific columns by replacing with column mean (excluding 0s)
    # Columns to check for 0s: Glucose (1), BloodPressure (2), SkinThickness (3), Insulin (4), BMI (5)
    cols_to_impute = [1, 2, 3, 4, 5]
    for col_idx in cols_to_impute:
        col_data = X[:, col_idx]
        non_zero_mean = np.mean(col_data[col_data != 0])
        X[:, col_idx] = np.where(X[:, col_idx] == 0, non_zero_mean, col_data)
    log_message("Handled zero values in features.")

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    log_message(f"Data split into training ({len(X_train)} samples) and testing ({len(X_test)} samples).")

    # Normalize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    log_message("Features scaled using StandardScaler.")

    # Convert to PyTorch tensors
    X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)
    log_message("Data converted to PyTorch tensors.")

    return X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor, len(feature_names)

# --- Main execution block (for direct script execution) ---
if __name__ == "__main__":
    # This is a placeholder for the data that would be passed from the tool.
    # In a real scenario, this script would receive the 'records' via an argument.
    # For testing, we'll use a dummy structure.
    dummy_records = [
        {"Age": 50, "BMI": 33.6, "BloodPressure": 72, "DiabetesPedigreeFunction": 0.627, "Glucose": 148, "Insulin": 0, "Outcome": 1, "Pregnancies": 6, "SkinThickness": 35, "_id": "1"},
        {"Age": 31, "BMI": 26.6, "BloodPressure": 66, "DiabetesPedigreeFunction": 0.351, "Glucose": 85, "Insulin": 0, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 29, "_id": "2"},
        {"Age": 32, "BMI": 23.3, "BloodPressure": 64, "DiabetesPedigreeFunction": 0.672, "Glucose": 183, "Insulin": 0, "Outcome": 1, "Pregnancies": 8, "SkinThickness": 0, "_id": "3"},
        {"Age": 21, "BMI": 28.1, "BloodPressure": 66, "DiabetesPedigreeFunction": 0.167, "Glucose": 89, "Insulin": 94, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 23, "_id": "4"},
        {"Age": 33, "BMI": 43.1, "BloodPressure": 40, "DiabetesPedigreeFunction": 2.288, "Glucose": 137, "Insulin": 168, "Outcome": 1, "Pregnancies": 0, "SkinThickness": 35, "_id": "5"},
        {"Age": 30, "BMI": 25.6, "BloodPressure": 74, "DiabetesPedigreeFunction": 0.201, "Glucose": 116, "Insulin": 0, "Outcome": 0, "Pregnancies": 5, "SkinThickness": 0, "_id": "6"},
        {"Age": 26, "BMI": 31, "BloodPressure": 50, "DiabetesPedigreeFunction": 0.248, "Glucose": 78, "Insulin": 88, "Outcome": 1, "Pregnancies": 3, "SkinThickness": 32, "_id": "7"},
        {"Age": 29, "BMI": 35.3, "BloodPressure": 0, "DiabetesPedigreeFunction": 0.134, "Glucose": 115, "Insulin": 0, "Outcome": 0, "Pregnancies": 10, "SkinThickness": 0, "_id": "8"},
        {"Age": 53, "BMI": 30.5, "BloodPressure": 70, "DiabetesPedigreeFunction": 0.158, "Glucose": 197, "Insulin": 543, "Outcome": 1, "Pregnancies": 2, "SkinThickness": 45, "_id": "9"},
        {"Age": 54, "BMI": 0, "BloodPressure": 96, "DiabetesPedigreeFunction": 0.232, "Glucose": 125, "Insulin": 0, "Outcome": 1, "Pregnancies": 8, "SkinThickness": 0, "_id": "10"},
        {"Age": 30, "BMI": 37.6, "BloodPressure": 92, "DiabetesPedigreeFunction": 0.191, "Glucose": 110, "Insulin": 0, "Outcome": 0, "Pregnancies": 4, "SkinThickness": 0, "_id": "11"},
        {"Age": 34, "BMI": 38, "BloodPressure": 74, "DiabetesPedigreeFunction": 0.537, "Glucose": 168, "Insulin": 0, "Outcome": 1, "Pregnancies": 10, "SkinThickness": 0, "_id": "12"},
        {"Age": 57, "BMI": 27.1, "BloodPressure": 80, "DiabetesPedigreeFunction": 1.441, "Glucose": 139, "Insulin": 0, "Outcome": 0, "Pregnancies": 10, "SkinThickness": 0, "_id": "13"},
        {"Age": 59, "BMI": 30.1, "BloodPressure": 60, "DiabetesPedigreeFunction": 0.398, "Glucose": 189, "Insulin": 846, "Outcome": 1, "Pregnancies": 1, "SkinThickness": 23, "_id": "14"},
        {"Age": 51, "BMI": 25.8, "BloodPressure": 72, "DiabetesPedigreeFunction": 0.587, "Glucose": 166, "Insulin": 175, "Outcome": 1, "Pregnancies": 5, "SkinThickness": 19, "_id": "15"},
        {"Age": 32, "BMI": 30, "BloodPressure": 0, "DiabetesPedigreeFunction": 0.484, "Glucose": 100, "Insulin": 0, "Outcome": 1, "Pregnancies": 7, "SkinThickness": 0, "_id": "16"},
        {"Age": 31, "BMI": 45.8, "BloodPressure": 84, "DiabetesPedigreeFunction": 0.551, "Glucose": 118, "Insulin": 230, "Outcome": 1, "Pregnancies": 0, "SkinThickness": 47, "_id": "17"},
        {"Age": 31, "BMI": 29.6, "BloodPressure": 74, "DiabetesPedigreeFunction": 0.254, "Glucose": 107, "Insulin": 0, "Outcome": 1, "Pregnancies": 7, "SkinThickness": 0, "_id": "18"},
        {"Age": 33, "BMI": 43.3, "BloodPressure": 30, "DiabetesPedigreeFunction": 0.183, "Glucose": 103, "Insulin": 83, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 38, "_id": "19"},
        {"Age": 32, "BMI": 34.6, "BloodPressure": 70, "DiabetesPedigreeFunction": 0.529, "Glucose": 115, "Insulin": 96, "Outcome": 1, "Pregnancies": 1, "SkinThickness": 30, "_id": "20"},
        {"Age": 27, "BMI": 39.3, "BloodPressure": 88, "DiabetesPedigreeFunction": 0.704, "Glucose": 126, "Insulin": 235, "Outcome": 0, "Pregnancies": 3, "SkinThickness": 41, "_id": "21"},
        {"Age": 50, "BMI": 35.4, "BloodPressure": 84, "DiabetesPedigreeFunction": 0.388, "Glucose": 99, "Insulin": 0, "Outcome": 0, "Pregnancies": 8, "SkinThickness": 0, "_id": "22"},
        {"Age": 41, "BMI": 39.8, "BloodPressure": 90, "DiabetesPedigreeFunction": 0.451, "Glucose": 196, "Insulin": 0, "Outcome": 1, "Pregnancies": 7, "SkinThickness": 0, "_id": "23"},
        {"Age": 29, "BMI": 29, "BloodPressure": 80, "DiabetesPedigreeFunction": 0.263, "Glucose": 119, "Insulin": 0, "Outcome": 1, "Pregnancies": 9, "SkinThickness": 35, "_id": "24"},
        {"Age": 51, "BMI": 36.6, "BloodPressure": 94, "DiabetesPedigreeFunction": 0.254, "Glucose": 143, "Insulin": 146, "Outcome": 1, "Pregnancies": 11, "SkinThickness": 33, "_id": "25"},
        {"Age": 41, "BMI": 31.1, "BloodPressure": 70, "DiabetesPedigreeFunction": 0.205, "Glucose": 125, "Insulin": 115, "Outcome": 1, "Pregnancies": 10, "SkinThickness": 26, "_id": "26"},
        {"Age": 43, "BMI": 39.4, "BloodPressure": 76, "DiabetesPedigreeFunction": 0.257, "Glucose": 147, "Insulin": 0, "Outcome": 1, "Pregnancies": 7, "SkinThickness": 0, "_id": "27"},
        {"Age": 22, "BMI": 23.2, "BloodPressure": 66, "DiabetesPedigreeFunction": 0.487, "Glucose": 97, "Insulin": 140, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 15, "_id": "28"},
        {"Age": 57, "BMI": 22.2, "BloodPressure": 82, "DiabetesPedigreeFunction": 0.245, "Glucose": 145, "Insulin": 110, "Outcome": 0, "Pregnancies": 13, "SkinThickness": 19, "_id": "29"},
        {"Age": 38, "BMI": 34.1, "BloodPressure": 92, "DiabetesPedigreeFunction": 0.337, "Glucose": 117, "Insulin": 0, "Outcome": 0, "Pregnancies": 5, "SkinThickness": 0, "_id": "30"},
        {"Age": 60, "BMI": 36, "BloodPressure": 75, "DiabetesPedigreeFunction": 0.546, "Glucose": 109, "Insulin": 0, "Outcome": 0, "Pregnancies": 5, "SkinThickness": 26, "_id": "31"},
        {"Age": 28, "BMI": 31.6, "BloodPressure": 76, "DiabetesPedigreeFunction": 0.851, "Glucose": 158, "Insulin": 245, "Outcome": 1, "Pregnancies": 3, "SkinThickness": 36, "_id": "32"},
        {"Age": 22, "BMI": 24.8, "BloodPressure": 58, "DiabetesPedigreeFunction": 0.267, "Glucose": 88, "Insulin": 54, "Outcome": 0, "Pregnancies": 3, "SkinThickness": 11, "_id": "33"},
        {"Age": 28, "BMI": 19.9, "BloodPressure": 92, "DiabetesPedigreeFunction": 0.188, "Glucose": 92, "Insulin": 0, "Outcome": 0, "Pregnancies": 6, "SkinThickness": 0, "_id": "34"},
        {"Age": 45, "BMI": 27.6, "BloodPressure": 78, "DiabetesPedigreeFunction": 0.512, "Glucose": 122, "Insulin": 0, "Outcome": 0, "Pregnancies": 10, "SkinThickness": 31, "_id": "35"},
        {"Age": 33, "BMI": 24, "BloodPressure": 60, "DiabetesPedigreeFunction": 0.966, "Glucose": 103, "Insulin": 192, "Outcome": 0, "Pregnancies": 4, "SkinThickness": 33, "_id": "36"},
        {"Age": 35, "BMI": 33.2, "BloodPressure": 76, "DiabetesPedigreeFunction": 0.42, "Glucose": 138, "Insulin": 0, "Outcome": 0, "Pregnancies": 11, "SkinThickness": 0, "_id": "37"},
        {"Age": 46, "BMI": 32.9, "BloodPressure": 76, "DiabetesPedigreeFunction": 0.665, "Glucose": 102, "Insulin": 0, "Outcome": 1, "Pregnancies": 9, "SkinThickness": 37, "_id": "38"},
        {"Age": 27, "BMI": 38.2, "BloodPressure": 68, "DiabetesPedigreeFunction": 0.503, "Glucose": 90, "Insulin": 0, "Outcome": 1, "Pregnancies": 2, "SkinThickness": 42, "_id": "39"},
        {"Age": 56, "BMI": 37.1, "BloodPressure": 72, "DiabetesPedigreeFunction": 1.39, "Glucose": 111, "Insulin": 207, "Outcome": 1, "Pregnancies": 4, "SkinThickness": 47, "_id": "40"},
        {"Age": 26, "BMI": 34, "BloodPressure": 64, "DiabetesPedigreeFunction": 0.271, "Glucose": 180, "Insulin": 70, "Outcome": 0, "Pregnancies": 3, "SkinThickness": 25, "_id": "41"},
        {"Age": 37, "BMI": 40.2, "BloodPressure": 84, "DiabetesPedigreeFunction": 0.696, "Glucose": 133, "Insulin": 0, "Outcome": 0, "Pregnancies": 7, "SkinThickness": 0, "_id": "42"},
        {"Age": 48, "BMI": 22.7, "BloodPressure": 92, "DiabetesPedigreeFunction": 0.235, "Glucose": 106, "Insulin": 0, "Outcome": 0, "Pregnancies": 7, "SkinThickness": 18, "_id": "43"},
        {"Age": 54, "BMI": 45.4, "BloodPressure": 110, "DiabetesPedigreeFunction": 0.721, "Glucose": 171, "Insulin": 240, "Outcome": 1, "Pregnancies": 9, "SkinThickness": 24, "_id": "44"},
        {"Age": 40, "BMI": 27.4, "BloodPressure": 64, "DiabetesPedigreeFunction": 0.294, "Glucose": 159, "Insulin": 0, "Outcome": 0, "Pregnancies": 7, "SkinThickness": 0, "_id": "45"},
        {"Age": 25, "BMI": 42, "BloodPressure": 66, "DiabetesPedigreeFunction": 1.893, "Glucose": 180, "Insulin": 0, "Outcome": 1, "Pregnancies": 0, "SkinThickness": 39, "_id": "46"},
        {"Age": 29, "BMI": 29.7, "BloodPressure": 56, "DiabetesPedigreeFunction": 0.564, "Glucose": 146, "Insulin": 0, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 0, "_id": "47"},
        {"Age": 22, "BMI": 28, "BloodPressure": 70, "DiabetesPedigreeFunction": 0.586, "Glucose": 71, "Insulin": 0, "Outcome": 0, "Pregnancies": 2, "SkinThickness": 27, "_id": "48"},
        {"Age": 31, "BMI": 39.1, "BloodPressure": 66, "DiabetesPedigreeFunction": 0.344, "Glucose": 103, "Insulin": 0, "Outcome": 1, "Pregnancies": 7, "SkinThickness": 32, "_id": "49"},
        {"Age": 24, "BMI": 0, "BloodPressure": 0, "DiabetesPedigreeFunction": 0.305, "Glucose": 105, "Insulin": 0, "Outcome": 0, "Pregnancies": 7, "SkinThickness": 0, "_id": "50"},
        {"Age": 22, "BMI": 19.4, "BloodPressure": 80, "DiabetesPedigreeFunction": 0.491, "Glucose": 103, "Insulin": 82, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 11, "_id": "51"},
        {"Age": 26, "BMI": 24.2, "BloodPressure": 50, "DiabetesPedigreeFunction": 0.526, "Glucose": 101, "Insulin": 36, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 15, "_id": "52"},
        {"Age": 30, "BMI": 24.4, "BloodPressure": 66, "DiabetesPedigreeFunction": 0.342, "Glucose": 88, "Insulin": 23, "Outcome": 0, "Pregnancies": 5, "SkinThickness": 21, "_id": "53"},
        {"Age": 58, "BMI": 33.7, "BloodPressure": 90, "DiabetesPedigreeFunction": 0.467, "Glucose": 176, "Insulin": 300, "Outcome": 1, "Pregnancies": 8, "SkinThickness": 34, "_id": "54"},
        {"Age": 42, "BMI": 34.7, "BloodPressure": 66, "DiabetesPedigreeFunction": 0.718, "Glucose": 150, "Insulin": 342, "Outcome": 0, "Pregnancies": 7, "SkinThickness": 42, "_id": "55"},
        {"Age": 21, "BMI": 23, "BloodPressure": 50, "DiabetesPedigreeFunction": 0.248, "Glucose": 73, "Insulin": 0, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 10, "_id": "56"},
        {"Age": 41, "BMI": 37.7, "BloodPressure": 68, "DiabetesPedigreeFunction": 0.254, "Glucose": 187, "Insulin": 304, "Outcome": 1, "Pregnancies": 7, "SkinThickness": 39, "_id": "57"},
        {"Age": 31, "BMI": 46.8, "BloodPressure": 88, "DiabetesPedigreeFunction": 0.962, "Glucose": 100, "Insulin": 110, "Outcome": 0, "Pregnancies": 0, "SkinThickness": 60, "_id": "58"},
        {"Age": 44, "BMI": 40.5, "BloodPressure": 82, "DiabetesPedigreeFunction": 1.781, "Glucose": 146, "Insulin": 0, "Outcome": 0, "Pregnancies": 0, "SkinThickness": 0, "_id": "59"},
        {"Age": 22, "BMI": 41.5, "BloodPressure": 64, "DiabetesPedigreeFunction": 0.173, "Glucose": 105, "Insulin": 142, "Outcome": 0, "Pregnancies": 0, "SkinThickness": 41, "_id": "60"},
        {"Age": 21, "BMI": 0, "BloodPressure": 0, "DiabetesPedigreeFunction": 0.304, "Glucose": 84, "Insulin": 0, "Outcome": 0, "Pregnancies": 2, "SkinThickness": 0, "_id": "61"},
        {"Age": 39, "BMI": 32.9, "BloodPressure": 72, "DiabetesPedigreeFunction": 0.27, "Glucose": 133, "Insulin": 0, "Outcome": 1, "Pregnancies": 8, "SkinThickness": 0, "_id": "62"},
        {"Age": 36, "BMI": 25, "BloodPressure": 62, "DiabetesPedigreeFunction": 0.587, "Glucose": 44, "Insulin": 0, "Outcome": 0, "Pregnancies": 5, "SkinThickness": 0, "_id": "63"},
        {"Age": 24, "BMI": 25.4, "BloodPressure": 58, "DiabetesPedigreeFunction": 0.699, "Glucose": 141, "Insulin": 128, "Outcome": 0, "Pregnancies": 2, "SkinThickness": 34, "_id": "64"},
        {"Age": 42, "BMI": 32.8, "BloodPressure": 66, "DiabetesPedigreeFunction": 0.258, "Glucose": 114, "Insulin": 0, "Outcome": 1, "Pregnancies": 7, "SkinThickness": 0, "_id": "65"},
        {"Age": 32, "BMI": 29, "BloodPressure": 74, "DiabetesPedigreeFunction": 0.203, "Glucose": 99, "Insulin": 0, "Outcome": 0, "Pregnancies": 5, "SkinThickness": 27, "_id": "66"},
        {"Age": 38, "BMI": 32.5, "BloodPressure": 88, "DiabetesPedigreeFunction": 0.855, "Glucose": 109, "Insulin": 0, "Outcome": 1, "Pregnancies": 0, "SkinThickness": 30, "_id": "67"},
        {"Age": 54, "BMI": 42.7, "BloodPressure": 92, "DiabetesPedigreeFunction": 0.845, "Glucose": 109, "Insulin": 0, "Outcome": 0, "Pregnancies": 2, "SkinThickness": 0, "_id": "68"},
        {"Age": 25, "BMI": 19.6, "BloodPressure": 66, "DiabetesPedigreeFunction": 0.334, "Glucose": 95, "Insulin": 38, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 13, "_id": "69"},
        {"Age": 27, "BMI": 28.9, "BloodPressure": 85, "DiabetesPedigreeFunction": 0.189, "Glucose": 146, "Insulin": 100, "Outcome": 0, "Pregnancies": 4, "SkinThickness": 27, "_id": "70"},
        {"Age": 28, "BMI": 32.9, "BloodPressure": 66, "DiabetesPedigreeFunction": 0.867, "Glucose": 100, "Insulin": 90, "Outcome": 1, "Pregnancies": 2, "SkinThickness": 20, "_id": "71"},
        {"Age": 26, "BMI": 28.6, "BloodPressure": 64, "DiabetesPedigreeFunction": 0.411, "Glucose": 139, "Insulin": 140, "Outcome": 0, "Pregnancies": 5, "SkinThickness": 35, "_id": "72"},
        {"Age": 42, "BMI": 43.4, "BloodPressure": 90, "DiabetesPedigreeFunction": 0.583, "Glucose": 126, "Insulin": 0, "Outcome": 1, "Pregnancies": 13, "SkinThickness": 0, "_id": "73"},
        {"Age": 23, "BMI": 35.1, "BloodPressure": 86, "DiabetesPedigreeFunction": 0.231, "Glucose": 129, "Insulin": 270, "Outcome": 0, "Pregnancies": 4, "SkinThickness": 20, "_id": "74"},
        {"Age": 22, "BMI": 32, "BloodPressure": 75, "DiabetesPedigreeFunction": 0.396, "Glucose": 79, "Insulin": 0, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 30, "_id": "75"},
        {"Age": 22, "BMI": 24.7, "BloodPressure": 48, "DiabetesPedigreeFunction": 0.14, "Glucose": 0, "Insulin": 0, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 20, "_id": "76"},
        {"Age": 41, "BMI": 32.6, "BloodPressure": 78, "DiabetesPedigreeFunction": 0.391, "Glucose": 62, "Insulin": 0, "Outcome": 0, "Pregnancies": 7, "SkinThickness": 0, "_id": "77"},
        {"Age": 27, "BMI": 37.7, "BloodPressure": 72, "DiabetesPedigreeFunction": 0.37, "Glucose": 95, "Insulin": 0, "Outcome": 0, "Pregnancies": 5, "SkinThickness": 33, "_id": "78"},
        {"Age": 26, "BMI": 43.2, "BloodPressure": 0, "DiabetesPedigreeFunction": 0.27, "Glucose": 131, "Insulin": 0, "Outcome": 1, "Pregnancies": 0, "SkinThickness": 0, "_id": "79"},
        {"Age": 24, "BMI": 25, "BloodPressure": 66, "DiabetesPedigreeFunction": 0.307, "Glucose": 112, "Insulin": 0, "Outcome": 0, "Pregnancies": 2, "SkinThickness": 22, "_id": "80"},
        {"Age": 22, "BMI": 22.4, "BloodPressure": 44, "DiabetesPedigreeFunction": 0.14, "Glucose": 113, "Insulin": 0, "Outcome": 0, "Pregnancies": 3, "SkinThickness": 13, "_id": "81"},
        {"Age": 22, "BMI": 0, "BloodPressure": 0, "DiabetesPedigreeFunction": 0.102, "Glucose": 74, "Insulin": 0, "Outcome": 0, "Pregnancies": 2, "SkinThickness": 0, "_id": "82"},
        {"Age": 36, "BMI": 29.3, "BloodPressure": 78, "DiabetesPedigreeFunction": 0.767, "Glucose": 83, "Insulin": 71, "Outcome": 0, "Pregnancies": 7, "SkinThickness": 26, "_id": "83"},
        {"Age": 22, "BMI": 24.6, "BloodPressure": 65, "DiabetesPedigreeFunction": 0.237, "Glucose": 101, "Insulin": 0, "Outcome": 0, "Pregnancies": 0, "SkinThickness": 28, "_id": "84"},
        {"Age": 37, "BMI": 48.8, "BloodPressure": 108, "DiabetesPedigreeFunction": 0.227, "Glucose": 137, "Insulin": 0, "Outcome": 1, "Pregnancies": 5, "SkinThickness": 0, "_id": "85"},
        {"Age": 27, "BMI": 32.4, "BloodPressure": 74, "DiabetesPedigreeFunction": 0.698, "Glucose": 110, "Insulin": 125, "Outcome": 0, "Pregnancies": 2, "SkinThickness": 29, "_id": "86"},
        {"Age": 45, "BMI": 36.6, "BloodPressure": 72, "DiabetesPedigreeFunction": 0.178, "Glucose": 106, "Insulin": 0, "Outcome": 0, "Pregnancies": 13, "SkinThickness": 54, "_id": "87"},
        {"Age": 26, "BMI": 38.5, "BloodPressure": 68, "DiabetesPedigreeFunction": 0.324, "Glucose": 100, "Insulin": 71, "Outcome": 0, "Pregnancies": 2, "SkinThickness": 25, "_id": "88"},
        {"Age": 43, "BMI": 37.1, "BloodPressure": 70, "DiabetesPedigreeFunction": 0.153, "Glucose": 136, "Insulin": 110, "Outcome": 1, "Pregnancies": 15, "SkinThickness": 32, "_id": "89"},
        {"Age": 24, "BMI": 26.5, "BloodPressure": 68, "DiabetesPedigreeFunction": 0.165, "Glucose": 107, "Insulin": 0, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 19, "_id": "90"},
        {"Age": 21, "BMI": 19.1, "BloodPressure": 55, "DiabetesPedigreeFunction": 0.258, "Glucose": 80, "Insulin": 0, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 0, "_id": "91"},
        {"Age": 34, "BMI": 32, "BloodPressure": 80, "DiabetesPedigreeFunction": 0.443, "Glucose": 123, "Insulin": 176, "Outcome": 0, "Pregnancies": 4, "SkinThickness": 15, "_id": "92"},
        {"Age": 42, "BMI": 46.7, "BloodPressure": 78, "DiabetesPedigreeFunction": 0.261, "Glucose": 81, "Insulin": 48, "Outcome": 0, "Pregnancies": 7, "SkinThickness": 40, "_id": "93"},
        {"Age": 60, "BMI": 23.8, "BloodPressure": 72, "DiabetesPedigreeFunction": 0.277, "Glucose": 134, "Insulin": 0, "Outcome": 1, "Pregnancies": 4, "SkinThickness": 0, "_id": "94"},
        {"Age": 21, "BMI": 24.7, "BloodPressure": 82, "DiabetesPedigreeFunction": 0.761, "Glucose": 142, "Insulin": 64, "Outcome": 0, "Pregnancies": 2, "SkinThickness": 18, "_id": "95"},
        {"Age": 40, "BMI": 33.9, "BloodPressure": 72, "DiabetesPedigreeFunction": 0.255, "Glucose": 144, "Insulin": 228, "Outcome": 0, "Pregnancies": 6, "SkinThickness": 27, "_id": "96"},
        {"Age": 24, "BMI": 31.6, "BloodPressure": 62, "DiabetesPedigreeFunction": 0.13, "Glucose": 92, "Insulin": 0, "Outcome": 0, "Pregnancies": 2, "SkinThickness": 28, "_id": "97"},
        {"Age": 22, "BMI": 20.4, "BloodPressure": 48, "DiabetesPedigreeFunction": 0.323, "Glucose": 71, "Insulin": 76, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 18, "_id": "98"},
        {"Age": 23, "BMI": 28.7, "BloodPressure": 50, "DiabetesPedigreeFunction": 0.356, "Glucose": 93, "Insulin": 64, "Outcome": 0, "Pregnancies": 6, "SkinThickness": 30, "_id": "99"},
        {"Age": 31, "BMI": 49.7, "BloodPressure": 90, "DiabetesPedigreeFunction": 0.325, "Glucose": 122, "Insulin": 220, "Outcome": 1, "Pregnancies": 1, "SkinThickness": 51, "_id": "100"}
    ]
    # In the actual execution, the records will be passed as a string argument.
    # For local testing, you can uncomment the line below and use dummy_records.
    # raw_records = json.dumps(dummy_records)
    # X_train, X_test, y_train, y_test, input_size = preprocess_data(raw_records)

    # When run via the tool, the first argument will be the JSON string of records.
    import sys
    raw_records = sys.argv[1]
    X_train, X_test, y_train, y_test, input_size = preprocess_data(raw_records)


    # --- 3. Model Parameters and Device Setup ---
    learning_rate = 0.001
    epochs = 1000
    batch_size = 16 # Using mini-batches for training

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    log_message(f"Using device: {device}")

    model = DiabetesClassifier(input_size).to(device)
    log_message(f"Model initialized: {model}")

    # Move data to the selected device
    X_train_tensor = X_train.to(device)
    y_train_tensor = y_train.to(device)
    X_test_tensor = X_test.to(device)
    y_test_tensor = y_test.to(device)

    # --- 4. Loss Function and Optimizer ---
    criterion = nn.BCEWithLogitsLoss() # Combines Sigmoid and BCELoss
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    log_message(f"Loss function: {criterion}")
    log_message(f"Optimizer: {optimizer}")

    # --- 5. Training Loop ---
    log_message("Starting training...")
    start_time = time.time()

    # Create DataLoader for batching
    train_dataset = torch.utils.data.TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    for epoch in range(epochs):
        model.train() # Set model to training mode
        for inputs, labels in train_loader:
            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if (epoch + 1) % 100 == 0:
            log_message(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")

    end_time = time.time()
    training_duration = end_time - start_time
    log_message("Training finished.")

    # --- 6. Benchmarking and Evaluation ---
    log_message("--- Benchmarking and Evaluation ---")

    # Evaluate on test set
    model.eval() # Set model to evaluation mode
    with torch.no_grad():
        test_outputs = model(X_test_tensor)
        test_loss = criterion(test_outputs, y_test_tensor).item()
        predicted_probs = torch.sigmoid(test_outputs)
        predicted_classes = (predicted_probs > 0.5).float()

        correct = (predicted_classes == y_test_tensor).sum().item()
        total = y_test_tensor.size(0)
        accuracy = correct / total

        log_message(f"Test Loss: {test_loss:.4f}")
        log_message(f"Accuracy on test data: {accuracy * 100:.2f}%")
        log_message(f"Total training time: {training_duration:.4f} seconds")

    # --- Print HTML summary for the user ---
    # Construct the HTML output string
    html_output = f"""
<div style="
    background-color:#1e293b;
    color:#f1f5f9;
    font-family:'Roboto', sans-serif;
    padding:20px;
    border-radius:8px;
    box-shadow:1px 2px 10px rgba(0,0,0,0.6);
    max-width:600px;
    margin:20px auto;
">
    <h2>Neural Network Model Training Results (Diabetes Prediction)</h2>
    <h3>Configuration:</h3>
    <ul>
        <li><strong>Model:</strong> Multi-Layer Perceptron (2 Hidden Layers)</li>
        <li><strong>Input Features:</strong> {input_size}</li>
        <li><strong>Hidden Layer 1 Size:</strong> 64</li>
        <li><strong>Hidden Layer 2 Size:</strong> 32</li>
        <li><strong>Output Size:</strong> 1 (Binary Classification)</li>
        <li><strong>Learning Rate:</strong> {learning_rate}</li>
        <li><strong>Epochs:</strong> {epochs}</li>
        <li><strong>Batch Size:</strong> {batch_size}</li>
        <li><strong>Device Used:</strong> {device}</li>
    </ul>
    <h3>Training Summary:</h3>
    <p>Training completed in <strong>{training_duration:.4f} seconds</strong>.</p>
    <h3>Final Evaluation on Test Set:</h3>
    <ul>
        <li><strong>Test Loss:</strong> <span style="color:#f97316; font-weight:bold;">{test_loss:.4f}</span></li>
        <li><strong>Accuracy:</strong> <span style="color:#4CAF50; font-weight:bold;">{accuracy * 100:.2f}%</span></li>
    </ul>
    <p>
        This model was trained to predict diabetes based on various health indicators.
        The accuracy on the test set provides an indication of how well the model generalizes
        to unseen data. Further hyperparameter tuning and model complexity adjustments
        could potentially improve performance.
    </p>
</div>
    """
    print(html_output)
