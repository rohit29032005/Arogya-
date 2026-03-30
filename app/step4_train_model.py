import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# 1. Load dataset
df = pd.read_csv("data/disease_symptom.csv")

# 2. Clean text
df["symptoms"] = df["symptoms"].astype(str).str.lower().str.strip()

# 3. Convert symptoms to TF-IDF features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["symptoms"])

# 4. Labels
y = df["disease"]

# 5. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# 6. Train Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X_train, y_train)

# 7. Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model training completed")
print("Accuracy:", accuracy)

# 8. Save model and vectorizer
joblib.dump(model, "model/random_forest_model.pkl")
joblib.dump(vectorizer, "model/tfidf_vectorizer.pkl")

print("Model and vectorizer saved successfully")
