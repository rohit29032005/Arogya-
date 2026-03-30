#for large model to make training more robust
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load LARGE dataset
df = pd.read_csv("data/disease_symptom_large.csv")

# Clean data
df = df.dropna(subset=["symptoms"])
df["symptoms"] = df["symptoms"].astype(str).str.lower().str.strip()

# TF-IDF
vectorizer = TfidfVectorizer(max_features=800)
X = vectorizer.fit_transform(df["symptoms"])
y = df["disease"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
accuracy = accuracy_score(y_test, model.predict(X_test))

print("Large Model Training Completed")
print("Accuracy:", accuracy)

# Save LARGE model separately
joblib.dump(model, "model/random_forest_large.pkl")
joblib.dump(vectorizer, "model/tfidf_large.pkl")

print("Large model and vectorizer saved")
