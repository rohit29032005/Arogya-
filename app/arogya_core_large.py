# import joblib
# import pandas as pd
# import numpy as np

# # Load ML components
# model = joblib.load("model/random_forest_large_smote.pkl")
# vectorizer = joblib.load("model/tfidf_large_smote.pkl")

# # Load Ayurveda DB
# ayurveda_df = pd.read_csv("data/ayurveda_large.csv")

# # 🔧 Normalize Ayurveda DB disease names
# ayurveda_df["disease"] = ayurveda_df["disease"].astype(str).str.lower().str.strip()

# print("=== AROGYA AI – Unified Large Scale Engine ===")

# # User inputs
# symptoms = input("Enter symptoms (comma separated): ").lower().strip()
# body_type = input("Enter body type (Vata / Pitta / Kapha): ").lower().strip()

# # Vectorize
# X_input = vectorizer.transform([symptoms])

# # Prediction probabilities
# probs = model.predict_proba(X_input)[0]
# classes = [c.lower().strip() for c in model.classes_]

# # Top 2 predictions
# order = np.argsort(probs)[::-1]
# top1, top2 = order[0], order[1]

# disease = classes[top1]
# gap = probs[top1] - probs[top2]

# # Confidence calibration
# if gap > 0.4:
#     confidence = "High"
# elif gap > 0.2:
#     confidence = "Medium"
# else:
#     confidence = "Low"

# print("\nPredicted Disease:", disease.title())
# print("Confidence Level:", confidence)

# # Ayurveda mapping (safe match)
# row = ayurveda_df[ayurveda_df["disease"] == disease]

# if not row.empty:
#     print("\nAyurvedic Recommendations:")
#     print("Herbs:", row["herbs"].values[0])
#     print("Therapy:", row["therapy"].values[0])
#     print("Diet:", row["diet"].values[0])

#     print("\nEffect on your body type:")
#     if body_type == "vata":
#         print(row["vata_effect"].values[0])
#     elif body_type == "pitta":
#         print(row["pitta_effect"].values[0])
#     elif body_type == "kapha":
#         print(row["kapha_effect"].values[0])
#     else:
#         print("General balancing effect")
# else:
#     print("\nAyurvedic data not found for this disease (category mapping missing).")

# print("\n⚠️ Disclaimer:")
# print("Educational & research use only. Consult a healthcare professional.")
################## error solved of disease ################no mapping in ayurveda_large.csv file#######################
import joblib
import pandas as pd
import numpy as np

# Load ML components
model = joblib.load("model/random_forest_large_smote.pkl")
vectorizer = joblib.load("model/tfidf_large_smote.pkl")

# Load Ayurveda DB (DIRECT DISEASE MAPPING)
ayurveda_df = pd.read_csv("data/ayurveda_templates.csv")

# Normalize disease names
ayurveda_df["disease"] = ayurveda_df["disease"].astype(str).str.lower().str.strip()

print("=== AROGYA AI – Unified Large Scale Engine ===")

# User inputs
symptoms = input("Enter symptoms (comma separated): ").lower().strip()
body_type = input("Enter body type (Vata / Pitta / Kapha): ").lower().strip()

# Vectorize
X_input = vectorizer.transform([symptoms])

# Prediction probabilities
probs = model.predict_proba(X_input)[0]
classes = [c.lower().strip() for c in model.classes_]

# Top predictions
order = np.argsort(probs)[::-1]
top1, top2 = order[0], order[1]

predicted_disease = classes[top1]
gap = probs[top1] - probs[top2]

# Confidence calibration
if gap > 0.4:
    confidence = "High"
elif gap > 0.2:
    confidence = "Medium"
else:
    confidence = "Low"

print("\nPredicted Disease:", predicted_disease.title())
print("Confidence Level:", confidence)

# Direct Ayurveda lookup
row = ayurveda_df[ayurveda_df["disease"] == predicted_disease]

if not row.empty:
    print("\nAyurvedic Recommendations:")
    print("Herbs:", row["herbs"].values[0])
    print("Therapy:", row["therapy"].values[0])
    print("Diet:", row["diet"].values[0])

    print("\nEffect on your body type:")
    if body_type == "vata":
        print(row["vata_effect"].values[0])
    elif body_type == "pitta":
        print(row["pitta_effect"].values[0])
    elif body_type == "kapha":
        print(row["kapha_effect"].values[0])
    else:
        print("General balancing effect")
else:
    print("\nAyurvedic data not found for this disease.")

print("\n Disclaimer:")
print("Educational & research use only. Consult a healthcare professional.")
