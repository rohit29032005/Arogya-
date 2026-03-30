import joblib

# Load LARGE model and vectorizer
model = joblib.load("model/random_forest_large.pkl")
vectorizer = joblib.load("model/tfidf_large.pkl")

print("=== AROGYA AI – Large Model Prediction Test ===")

user_symptoms = input("Enter symptoms: ").lower().strip()

X_input = vectorizer.transform([user_symptoms])

prediction = model.predict(X_input)[0]
probs = model.predict_proba(X_input)[0]

confidence = max(probs) * 100

print("\nPredicted Disease:", prediction)
print("Raw Confidence:", round(confidence, 2), "%")
