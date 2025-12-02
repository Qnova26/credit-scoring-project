import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import random
import numpy as np
import os
import warnings
import sys

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    # MENERIMA INPUT DARI SYSTEM (DARI FILE MLPROJECT)
    # Urutan indeks [1], [2], [3] harus sesuai urutan di command MLproject
    
    # Ambil nilai n_estimators (jika tidak ada, default 505)
    n_estimators = int(sys.argv[1]) if len(sys.argv) > 1 else 505
    
    # Ambil nilai max_depth (jika tidak ada, default 37)
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 37
    
    # Ambil lokasi dataset
    file_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "train_pca.csv")

    print(f"Mulai Training dengan: n_estimators={n_estimators}, max_depth={max_depth}")

    # Baca Data
    data = pd.read_csv(file_path)

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        data.drop("Credit_Score", axis=1),
        data["Credit_Score"],
        random_state=42,
        test_size=0.2
    )
    
    input_example = X_train[0:5]

    # MULAI TRACKING (Tanpa set_tracking_uri)
    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
        
        # Latih Model
        model.fit(X_train, y_train)

        # Log Model ke Artifact
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            input_example=input_example
        )

        # Log Metrics
        accuracy = model.score(X_test, y_test)
        mlflow.log_metric("accuracy", accuracy)
        
        print(f"Training Selesai. Akurasi: {accuracy}")