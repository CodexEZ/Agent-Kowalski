
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json

def train_and_evaluate_nn(records):
    df = pd.DataFrame(records)

    # Drop the _id column as it is not a feature
    df = df.drop(columns=["_id"])

    # Define features (X) and target (y)
    X = df.drop("Outcome", axis=1)  # All columns except "Outcome"
    y = df["Outcome"]  # The "Outcome" column is the target

    # Handle potential missing values by filling with the mean (a simple approach)
    X = X.fillna(X.mean())

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Initialize and train the MLPClassifier (Neural Network)
    mlp = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=1000, random_state=42)
    mlp.fit(X_train_scaled, y_train)

    # Make predictions on the test set
    y_pred = mlp.predict(X_test_scaled)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    results = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "model_parameters": mlp.get_params()
    }
    print(json.dumps(results))

# The actual data will be passed when running the script.
# For now, this is just the function definition.
