import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, precision_recall_curve, precision_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import os

try:
    # 1. Daten laden
    data_path = "6.4.2025_ml_datenv2.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Datei {data_path} nicht gefunden!")
    
    df = pd.read_csv(data_path)
    
    # 2. Datenvorverarbeitung
    target_column = "acquired_or_closed"
    
    # Überprüfen, ob die Zielspalte existiert
    if target_column not in df.columns:
        raise ValueError(f"Zielspalte '{target_column}' nicht in den Daten gefunden!")
    
    # Features und Zielvariable trennen
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # Fehlende Werte behandeln
    imputer = SimpleImputer(strategy='mean')
    X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
    
    # Daten skalieren
    scaler = StandardScaler()
    X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    
    # 3. Train-Test-Split
    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 4. Modelltraining mit Hyperparameter-Optimierung
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0]
    }
    
    model = xgb.XGBClassifier(
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42
    )
    
    grid_search = GridSearchCV(
        model, param_grid, cv=5, scoring='precision', n_jobs=-1
    )
    grid_search.fit(X_train, y_train)
    
    # Bestes Modell auswählen
    best_model = grid_search.best_estimator_
    print(f"Beste Parameter: {grid_search.best_params_}")
    
    # 5. Vorhersagen
    y_proba = best_model.predict_proba(X_valid)[:, 1]
    
    # 6. Besten Schwellenwert für Precision finden
    precision, recall, thresholds = precision_recall_curve(y_valid, y_proba)
    best_threshold = thresholds[precision.argmax()]
    print(f"🔍 Bester Schwellenwert für maximale Precision: {best_threshold:.2f}")
    
    # 7. Schwellenwert anwenden
    y_pred = (y_proba > best_threshold).astype(int)
    
    # 8. Evaluation
    print("\n📊 Klassifikationsbericht (Optimiert für Precision):")
    print(classification_report(y_valid, y_pred))
    print("Precision:", precision_score(y_valid, y_pred))
    
    # 9. Precision-Recall-Kurve plotten
    plt.figure(figsize=(10, 6))
    plt.plot(thresholds, precision[:-1], label='Precision')
    plt.plot(thresholds, recall[:-1], label='Recall')
    plt.xlabel("Schwellenwert")
    plt.ylabel("Score")
    plt.title("Precision vs Recall vs Schwellenwert")
    plt.legend()
    plt.grid(True)
    plt.show()

except FileNotFoundError as e:
    print(f"Fehler: {e}")
except ValueError as e:
    print(f"Fehler: {e}")
except Exception as e:
    print(f"Unerwarteter Fehler: {e}")
