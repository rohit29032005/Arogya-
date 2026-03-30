import joblib
import numpy as np

# Load SMOTE-trained large model
model = joblib.load("model/random_forest_large_smote.pkl")
vectorizer = joblib.load("model/tfidf_large_smote.pkl")

print("=== AROGYA AI – Large Scale Disease Prediction (SMOTE Model) ===")

# User input
user_symptoms = input("Enter symptoms (comma separated): ").lower().strip()

# Vectorize input
X_input = vectorizer.transform([user_symptoms])

# Get probabilities
probs = model.predict_proba(X_input)[0]
classes = model.classes_

# Sort predictions
sorted_idx = np.argsort(probs)[::-1]
top1, top2 = sorted_idx[0], sorted_idx[1]

predicted_disease = classes[top1]
gap = probs[top1] - probs[top2]

# Confidence calibration
if gap > 0.4:
    confidence = "High"
elif gap > 0.2:
    confidence = "Medium"
else:
    confidence = "Low"

print("\nPredicted Disease:", predicted_disease)
print("Confidence Level:", confidence)

print("\n Disclaimer:")
print("This prediction is for educational and research purposes only.")
print("Consult a qualified healthcare professional for medical advice.")
