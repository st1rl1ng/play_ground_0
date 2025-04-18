import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

data_path = "6.4.2025_ml_datenv2.csv"

df = pd.read_csv(data_path)

# 🔹 2. Define features & target
target_column = "acquired_or_closed"  # <-- Replace with your actual label column
X = df.drop(columns=[target_column])
y = df[target_column]

# 🔹 3. Train-test split
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔹 4. Train XGBoost
model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    use_label_encoder=False,
    eval_metric='logloss'
)
model.fit(X_train, y_train)

# 🔹 5. Predict probabilities
y_proba = model.predict_proba(X_valid)[:, 1]

# 🔹 6. Find best threshold for precision
precision, recall, thresholds = precision_recall_curve(y_valid, y_proba)
best_threshold = thresholds[precision.argmax()]
print(f"🔍 Best threshold for max precision: {best_threshold:.2f}")

# 🔹 7. Apply best threshold
y_pred = (y_proba > best_threshold).astype(int)

# 🔹 8. Evaluate
print("\n📊 Classification Report (Optimized for Precision):")
print(classification_report(y_valid, y_pred))
print("Precision:", precision_score(y_valid, y_pred))

# 🔹 9. Optional: Plot Precision-Recall curve
plt.plot(thresholds, precision[:-1], label='Precision')
plt.plot(thresholds, recall[:-1], label='Recall')
plt.xlabel("Threshold")
plt.ylabel("Score")
plt.title("Precision vs Recall vs Threshold")
plt.legend()
plt.grid(True)
plt.show()
