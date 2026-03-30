# import joblib

# # 1. Load trained model and vectorizer
# model = joblib.load("model/random_forest_model.pkl")
# vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

# print("=== AROGYA AI – Disease Prediction ===")

# # 2. Take user input
# user_symptoms = input("Enter your symptoms (comma separated): ")

# # 3. Clean input
# user_symptoms = user_symptoms.lower().strip()

# # 4. Convert input to TF-IDF
# X_input = vectorizer.transform([user_symptoms])

# # 5. Predict disease
# prediction = model.predict(X_input)[0]

# # 6. Prediction probability
# confidence = model.predict_proba(X_input).max() * 100

# print("\nPredicted Disease:", prediction)
# print("Confidence:", round(confidence, 2), "%")

#new code after the auryvedic basic addition
# import joblib
# import pandas as pd

# # Load ML model and vectorizer
# model = joblib.load("model/random_forest_model.pkl")
# vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

# # Load Ayurvedic database
# ayurveda_df = pd.read_csv("data/ayurveda_basic.csv")

# print("=== AROGYA AI – Disease Prediction with Ayurvedic Advice ===")

# # User input
# user_symptoms = input("Enter your symptoms (comma separated): ").lower().strip()

# # Vectorize input
# X_input = vectorizer.transform([user_symptoms])

# # Predict disease
# prediction = model.predict(X_input)[0]
# confidence = model.predict_proba(X_input).max() * 100

# print("\nPredicted Disease:", prediction)
# print("Confidence:", round(confidence, 2), "%")

# # Fetch Ayurvedic recommendation
# treatment = ayurveda_df[ayurveda_df["disease"] == prediction]

# if not treatment.empty:
#     print("\nAyurvedic Recommendations:")
#     print("Herbs:", treatment["herbs"].values[0])
#     print("Therapy:", treatment["therapy"].values[0])
#     print("Diet:", treatment["diet"].values[0])
# else:
#     print("\nNo Ayurvedic data available for this disease.")

#new code after the auryvedic basic addition with error handling
# import joblib
# import pandas as pd

# # Load ML model and vectorizer
# model = joblib.load("model/random_forest_model.pkl")
# vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

# # Load Ayurvedic database
# ayurveda_df = pd.read_csv("data/ayurveda_basic.csv")

# print("=== AROGYA AI – Personalized Disease Prediction ===")

# # User inputs
# user_symptoms = input("Enter your symptoms (comma separated): ").lower().strip()
# body_type = input("Enter your body type (Vata / Pitta / Kapha): ").strip().lower()

# # Vectorize input
# X_input = vectorizer.transform([user_symptoms])

# # Predict disease
# prediction = model.predict(X_input)[0]
# confidence = model.predict_proba(X_input).max() * 100

# print("\nPredicted Disease:", prediction)
# print("Confidence:", round(confidence, 2), "%")

# # Fetch Ayurvedic recommendation
# treatment = ayurveda_df[ayurveda_df["disease"] == prediction]

# if not treatment.empty:
#     print("\nAyurvedic Recommendations:")
#     print("Herbs:", treatment["herbs"].values[0])
#     print("Therapy:", treatment["therapy"].values[0])
#     print("Diet:", treatment["diet"].values[0])

#     print("\nHow this treatment helps your body type:")
#     if body_type == "vata":
#         print(treatment["vata_effect"].values[0])
#     elif body_type == "pitta":
#         print(treatment["pitta_effect"].values[0])
#     elif body_type == "kapha":
#         print(treatment["kapha_effect"].values[0])
#     else:
#         print("General balancing effect on the body")
# else:
#     print("\nNo Ayurvedic data available for this disease.")
import joblib
import pandas as pd
import numpy as np

# Load ML model and vectorizer
model = joblib.load("model/random_forest_model.pkl")
vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

# Load Ayurvedic database
ayurveda_df = pd.read_csv("data/ayurveda_basic.csv")

print("=== AROGYA AI – Personalized Disease Prediction System ===")

# User inputs
user_symptoms = input("Enter your symptoms (comma separated): ").lower().strip()
body_type = input("Enter your body type (Vata / Pitta / Kapha): ").strip().lower()

# Vectorize input
X_input = vectorizer.transform([user_symptoms])

# Predict probabilities
probs = model.predict_proba(X_input)[0]
classes = model.classes_

# Get top 2 predictions
top_indices = np.argsort(probs)[::-1]
top1, top2 = top_indices[0], top_indices[1]

predicted_disease = classes[top1]
gap = probs[top1] - probs[top2]

# Confidence calibration
if gap > 0.4:
    confidence_level = "High"
elif gap > 0.2:
    confidence_level = "Medium"
else:
    confidence_level = "Low"

print("\nPredicted Disease:", predicted_disease)
print("Confidence Level:", confidence_level)

# Fetch Ayurvedic recommendation
treatment = ayurveda_df[ayurveda_df["disease"] == predicted_disease]

if not treatment.empty:
    print("\nAyurvedic Recommendations:")
    print("Herbs:", treatment["herbs"].values[0])
    print("Therapy:", treatment["therapy"].values[0])
    print("Diet:", treatment["diet"].values[0])

    print("\nHow this treatment helps your body type:")
    if body_type == "vata":
        print(treatment["vata_effect"].values[0])
    elif body_type == "pitta":
        print(treatment["pitta_effect"].values[0])
    elif body_type == "kapha":
        print(treatment["kapha_effect"].values[0])
    else:
        print("General balancing effect on the body")

print("\n⚠️ Disclaimer:")
print("This system is for educational purposes only.")
print("Please consult a qualified healthcare professional for medical advice.")
