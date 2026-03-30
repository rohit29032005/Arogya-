# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import joblib
# import pandas as pd
# import numpy as np

# app = Flask(__name__)
# CORS(app)

# # Load ML components
# model = joblib.load("../model/random_forest_large_smote.pkl")
# vectorizer = joblib.load("../model/tfidf_large_smote.pkl")

# # Load Ayurveda DB
# ayurveda_df = pd.read_csv("../data/ayurveda_templates.csv")
# ayurveda_df["disease"] = ayurveda_df["disease"].astype(str).str.lower().str.strip()

# @app.route("/")
# def home():
#     return {"message": "Arogya AI Backend Running"}

# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.json

#     symptoms = data.get("symptoms", "").lower().strip()
#     body_type = data.get("body_type", "").lower().strip()

#     if not symptoms:
#         return jsonify({"error": "Symptoms are required"}), 400

#     X_input = vectorizer.transform([symptoms])

#     probs = model.predict_proba(X_input)[0]
#     classes = [c.lower().strip() for c in model.classes_]

#     order = np.argsort(probs)[::-1]
#     top1, top2 = order[0], order[1]

#     disease = classes[top1]
#     gap = probs[top1] - probs[top2]

#     if gap > 0.4:
#         confidence = "High"
#     elif gap > 0.2:
#         confidence = "Medium"
#     else:
#         confidence = "Low"

#     response = {
#         "predicted_disease": disease.title(),
#         "confidence": confidence
#     }

#     row = ayurveda_df[ayurveda_df["disease"] == disease]

#     if not row.empty:
#         response["ayurveda"] = {
#             "herbs": row["herbs"].values[0],
#             "therapy": row["therapy"].values[0],
#             "diet": row["diet"].values[0],
#             "body_type_effect": (
#                 row["vata_effect"].values[0] if body_type == "vata"
#                 else row["pitta_effect"].values[0] if body_type == "pitta"
#                 else row["kapha_effect"].values[0] if body_type == "kapha"
#                 else "General balancing effect"
#             )
#         }
#     else:
#         response["ayurveda"] = "No data available"

#     response["disclaimer"] = "Educational & research use only"

#     return jsonify(response)

# if __name__ == "__main__":
#     app.run(debug=True)
##### for new agentic mode backend/app.py #####
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import joblib
# import os
# import pandas as pd

# app = Flask(__name__)
# CORS(app)

# # -------------------------------------------------
# # PATHS
# # -------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MODEL_DIR = os.path.join(BASE_DIR, "model")
# DATA_DIR = os.path.join(BASE_DIR, "data")

# # -------------------------------------------------
# # LOAD ML MODEL
# # -------------------------------------------------
# model = joblib.load(os.path.join(MODEL_DIR, "random_forest_large_smote.pkl"))
# vectorizer = joblib.load(os.path.join(MODEL_DIR, "tfidf_large_smote.pkl"))

# # -------------------------------------------------
# # LOAD CSVs
# # -------------------------------------------------
# disease_category_df = pd.read_csv(os.path.join(DATA_DIR, "ayurveda_large.csv"))
# templates_df = pd.read_csv(os.path.join(DATA_DIR, "ayurveda_templates.csv"))

# # Normalize text
# disease_category_df["disease"] = disease_category_df["disease"].str.strip()
# disease_category_df["category"] = disease_category_df["category"].str.strip()

# templates_df["disease"] = templates_df["disease"].str.strip()

# # -------------------------------------------------
# # CONFIG
# # -------------------------------------------------
# HIGH_CONF = 80

# # -------------------------------------------------
# # GENERIC DOCTOR QUESTIONS
# # -------------------------------------------------
# GENERIC_QUESTIONS = [
#     {"id": "chronic", "question": "Kya ye problem kaafi time se chal rahi hai?"},
#     {"id": "fatigue", "question": "Kya aapko roz thakan mehsoos hoti hai?"},
#     {"id": "progressive", "question": "Kya symptoms dheere-dheere badhte ja rahe hain?"}
# ]

# # -------------------------------------------------
# # UTILITY FUNCTIONS
# # -------------------------------------------------
# def calculate_confidence(prob):
#     return int(prob * 100)

# def update_confidence(base, answers):
#     boost = sum(5 for v in answers.values() if v.lower() == "yes")
#     return min(base + boost, 95)

# def get_category(disease):
#     row = disease_category_df[disease_category_df["disease"] == disease]
#     if row.empty:
#         return None
#     return row.iloc[0]["category"]

# def get_ayurveda_by_disease(disease):
#     row = templates_df[templates_df["disease"] == disease]
#     if row.empty:
#         return None
#     return row.iloc[0]

# def get_ayurveda_by_category(category):
#     row = templates_df[templates_df["category"] == category]
#     if row.empty:
#         return None
#     return row.iloc[0]

# def build_ayurveda_response(disease, body_type):
#     body_type = body_type.lower()

#     # 1️⃣ Try disease-specific Ayurveda
#     ayu = get_ayurveda_by_disease(disease)

#     # 2️⃣ If not found, use category-based Ayurveda
#     if ayu is None:
#         category = get_category(disease)
#         ayu = get_ayurveda_by_category(category)

#     # 3️⃣ Final safety fallback (should rarely happen)
#     if ayu is None:
#         return {
#             "herbs": "Guduchi, Triphala",
#             "therapy": "Abhyanga, Panchakarma",
#             "diet": "Light, warm, sattvic diet",
#             "body_type_effect": "Helps balance doshas and improve overall health"
#         }

#     effect_col = f"{body_type}_effect"
#     effect = ayu[effect_col] if effect_col in ayu and pd.notna(ayu[effect_col]) else "Helps balance dosha"

#     return {
#         "herbs": ayu["herbs"],
#         "therapy": ayu["therapy"],
#         "diet": ayu["diet"],
#         "body_type_effect": effect
#     }

# # -------------------------------------------------
# # ROUTES
# # -------------------------------------------------
# @app.route("/")
# def home():
#     return {"message": "Arogya AI Backend Running"}

# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.json

#     symptoms = data.get("symptoms", "")
#     body_type = data.get("body_type", "vata")
#     answers = data.get("answers")
#     locked_disease = data.get("locked_disease")

#     # ---------------------------
#     # FIRST CALL → ML PREDICTION
#     # ---------------------------
#     if not locked_disease:
#         X = vectorizer.transform([symptoms])
#         probs = model.predict_proba(X)[0]
#         idx = probs.argmax()

#         disease = model.classes_[idx]
#         confidence = calculate_confidence(probs[idx])

#         if confidence < HIGH_CONF:
#             return jsonify({
#                 "status": "need_clarification",
#                 "predicted_disease": disease,
#                 "confidence": confidence,
#                 "questions": GENERIC_QUESTIONS
#             })
#     else:
#         disease = locked_disease
#         confidence = 60

#     # ---------------------------
#     # CONFIRMATION PHASE
#     # ---------------------------
#     if answers:
#         confidence = update_confidence(confidence, answers)

#     # ---------------------------
#     # AYURVEDA RESPONSE
#     # ---------------------------
#     ayurveda = build_ayurveda_response(disease, body_type)

#     return jsonify({
#         "status": "final",
#         "predicted_disease": disease,
#         "confidence": "High" if confidence >= HIGH_CONF else "Medium",
#         "ayurveda": ayurveda,
#         "disclaimer": "Educational & research use only. Consult a healthcare professional."
#     })

# # -------------------------------------------------
# if __name__ == "__main__":
#     app.run(debug=True)



###############now code for contradicting agentic mode backend/app.py###############

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import joblib
# import os
# import pandas as pd

# app = Flask(__name__)
# CORS(app)

# # -------------------------------------------------
# # PATHS
# # -------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MODEL_DIR = os.path.join(BASE_DIR, "model")
# DATA_DIR = os.path.join(BASE_DIR, "data")

# # -------------------------------------------------
# # LOAD ML MODEL
# # -------------------------------------------------
# model = joblib.load(os.path.join(MODEL_DIR, "random_forest_large_smote.pkl"))
# vectorizer = joblib.load(os.path.join(MODEL_DIR, "tfidf_large_smote.pkl"))

# # -------------------------------------------------
# # LOAD CSVs
# # -------------------------------------------------
# disease_category_df = pd.read_csv(os.path.join(DATA_DIR, "ayurveda_large.csv"))
# templates_df = pd.read_csv(os.path.join(DATA_DIR, "ayurveda_templates.csv"))

# disease_category_df["disease"] = disease_category_df["disease"].str.strip()
# disease_category_df["category"] = disease_category_df["category"].str.strip()
# templates_df["disease"] = templates_df["disease"].str.strip()

# # -------------------------------------------------
# HIGH_CONF = 80
# REJECT_THRESHOLD = 2  # number of "NO" answers to reject hypothesis
# # -------------------------------------------------

# GENERIC_QUESTIONS = [
#     {"id": "chronic", "question": "Kya ye problem kaafi time se chal rahi hai?"},
#     {"id": "fatigue", "question": "Kya aapko roz thakan mehsoos hoti hai?"},
#     {"id": "progressive", "question": "Kya symptoms dheere-dheere badhte ja rahe hain?"}
# ]

# # -------------------------------------------------
# def calculate_confidence(prob):
#     return int(prob * 100)

# def update_confidence(base, answers):
#     boost = sum(5 for v in answers.values() if v.lower() == "yes")
#     return min(base + boost, 95)

# def count_negative_answers(answers):
#     return sum(1 for v in answers.values() if v.lower() == "no")

# def get_category(disease):
#     row = disease_category_df[disease_category_df["disease"] == disease]
#     return None if row.empty else row.iloc[0]["category"]

# def get_ayurveda(disease, body_type):
#     body_type = body_type.lower()

#     row = templates_df[templates_df["disease"] == disease]
#     if row.empty:
#         category = get_category(disease)
#         row = templates_df[templates_df["category"] == category]

#     if row.empty:
#         return {
#             "herbs": "Guduchi, Triphala",
#             "therapy": "Abhyanga, Panchakarma",
#             "diet": "Light, warm, sattvic diet",
#             "body_type_effect": "Helps balance doshas"
#         }

#     row = row.iloc[0]
#     effect = row.get(f"{body_type}_effect", "Balances dosha")

#     return {
#         "herbs": row["herbs"],
#         "therapy": row["therapy"],
#         "diet": row["diet"],
#         "body_type_effect": effect
#     }

# # -------------------------------------------------
# @app.route("/")
# def home():
#     return {"message": "Arogya AI Backend Running"}

# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.json

#     symptoms = data.get("symptoms", "")
#     body_type = data.get("body_type", "vata")
#     answers = data.get("answers")
#     locked_disease = data.get("locked_disease")

#     # ---------------------------
#     # FIRST CALL
#     # ---------------------------
#     if not locked_disease:
#         X = vectorizer.transform([symptoms])
#         probs = model.predict_proba(X)[0]
#         idx = probs.argmax()

#         disease = model.classes_[idx]
#         confidence = calculate_confidence(probs[idx])

#         if confidence < HIGH_CONF:
#             return jsonify({
#                 "status": "need_clarification",
#                 "predicted_disease": disease,
#                 "confidence": confidence,
#                 "questions": GENERIC_QUESTIONS
#             })
#     else:
#         disease = locked_disease
#         confidence = 60

#     # ---------------------------
#     # CONTRADICTION CHECK
#     # ---------------------------
#     if answers:
#         negative_count = count_negative_answers(answers)

#         if negative_count >= REJECT_THRESHOLD:
#             return jsonify({
#                 "status": "hypothesis_rejected",
#                 "message": "Aapke jawab is diagnosis ko support nahi kar rahe. Kisi aur condition ki possibility ho sakti hai.",
#                 "suggestion": "Please review symptoms or consider professional consultation."
#             })

#         confidence = update_confidence(confidence, answers)

#     # ---------------------------
#     ayurveda = get_ayurveda(disease, body_type)

#     return jsonify({
#         "status": "final",
#         "predicted_disease": disease,
#         "confidence": "High" if confidence >= HIGH_CONF else "Medium",
#         "ayurveda": ayurveda,
#         "disclaimer": "Educational & research use only. Consult a healthcare professional."
#     })

# # -------------------------------------------------
# if __name__ == "__main__":
#     app.run(debug=True)

#now codw will give 2 best disease if hypothesis is rejected for the first one

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import joblib
# import os
# import pandas as pd
# import numpy as np

# app = Flask(__name__)
# CORS(app)

# # -------------------------------------------------
# # PATHS
# # -------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MODEL_DIR = os.path.join(BASE_DIR, "model")
# DATA_DIR = os.path.join(BASE_DIR, "data")

# # -------------------------------------------------
# # LOAD ML
# # -------------------------------------------------
# model = joblib.load(os.path.join(MODEL_DIR, "random_forest_large_smote.pkl"))
# vectorizer = joblib.load(os.path.join(MODEL_DIR, "tfidf_large_smote.pkl"))

# # -------------------------------------------------
# # LOAD CSVs
# # -------------------------------------------------
# disease_category_df = pd.read_csv(os.path.join(DATA_DIR, "ayurveda_large.csv"))
# templates_df = pd.read_csv(os.path.join(DATA_DIR, "ayurveda_templates.csv"))

# disease_category_df["disease"] = disease_category_df["disease"].str.strip()
# disease_category_df["category"] = disease_category_df["category"].str.strip()
# templates_df["disease"] = templates_df["disease"].str.strip()

# # -------------------------------------------------
# HIGH_CONF = 80
# REJECT_THRESHOLD = 2
# # -------------------------------------------------

# GENERIC_QUESTIONS = [
#     {"id": "chronic", "question": "Kya ye problem kaafi time se chal rahi hai?"},
#     {"id": "fatigue", "question": "Kya aapko roz thakan mehsoos hoti hai?"},
#     {"id": "progressive", "question": "Kya symptoms dheere-dheere badhte ja rahe hain?"}
# ]

# # -------------------------------------------------
# def calculate_confidence(prob):
#     return int(prob * 100)

# def update_confidence(base, answers):
#     boost = sum(5 for v in answers.values() if v.lower() == "yes")
#     return min(base + boost, 95)

# def count_negative_answers(answers):
#     return sum(1 for v in answers.values() if v.lower() == "no")

# def get_category(disease):
#     row = disease_category_df[disease_category_df["disease"] == disease]
#     return None if row.empty else row.iloc[0]["category"]

# def get_ayurveda(disease, body_type):
#     body_type = body_type.lower()

#     row = templates_df[templates_df["disease"] == disease]
#     if row.empty:
#         category = get_category(disease)
#         row = templates_df[templates_df["category"] == category]

#     if row.empty:
#         return {
#             "herbs": "Guduchi, Triphala",
#             "therapy": "Abhyanga, Panchakarma",
#             "diet": "Light, warm, sattvic diet",
#             "body_type_effect": "Helps balance doshas"
#         }

#     row = row.iloc[0]
#     effect = row.get(f"{body_type}_effect", "Balances dosha")

#     return {
#         "herbs": row["herbs"],
#         "therapy": row["therapy"],
#         "diet": row["diet"],
#         "body_type_effect": effect
#     }

# # -------------------------------------------------
# @app.route("/")
# def home():
#     return {"message": "Arogya AI Backend Running"}

# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.json

#     symptoms = data.get("symptoms", "")
#     body_type = data.get("body_type", "vata")
#     answers = data.get("answers")
#     locked_disease = data.get("locked_disease")

#     # ---------------------------
#     # FIRST CALL
#     # ---------------------------
#     if not locked_disease:
#         X = vectorizer.transform([symptoms])
#         probs = model.predict_proba(X)[0]

#         top_indices = np.argsort(probs)[::-1]
#         primary_idx = top_indices[0]
#         secondary_idx = top_indices[1]

#         disease = model.classes_[primary_idx]
#         alt_disease = model.classes_[secondary_idx]

#         confidence = calculate_confidence(probs[primary_idx])

#         if confidence < HIGH_CONF:
#             return jsonify({
#                 "status": "need_clarification",
#                 "predicted_disease": disease,
#                 "confidence": confidence,
#                 "questions": GENERIC_QUESTIONS,
#                 "alternative_candidate": alt_disease
#             })
#     else:
#         disease = locked_disease
#         confidence = 60

#     # ---------------------------
#     # CONTRADICTION HANDLING
#     # ---------------------------
#     if answers:
#         negative_count = count_negative_answers(answers)

#         if negative_count >= REJECT_THRESHOLD:
#             # Suggest alternative disease
#             X = vectorizer.transform([symptoms])
#             probs = model.predict_proba(X)[0]
#             top_indices = np.argsort(probs)[::-1]

#             alt_disease = model.classes_[top_indices[1]]
#             alt_ayurveda = get_ayurveda(alt_disease, body_type)

#             return jsonify({
#                 "status": "alternative_suggested",
#                 "rejected_disease": disease,
#                 "alternative_disease": alt_disease,
#                 "ayurveda": alt_ayurveda,
#                 "message": "Pehli diagnosis match nahi hui. Ek aur possible condition suggest ki ja rahi hai.",
#                 "disclaimer": "Educational & research use only. Consult a healthcare professional."
#             })

#         confidence = update_confidence(confidence, answers)

#     # ---------------------------
#     ayurveda = get_ayurveda(disease, body_type)

#     return jsonify({
#         "status": "final",
#         "predicted_disease": disease,
#         "confidence": "High" if confidence >= HIGH_CONF else "Medium",
#         "ayurveda": ayurveda,
#         "disclaimer": "Educational & research use only. Consult a healthcare professional."
#     })

# # -------------------------------------------------
# if __name__ == "__main__":
#     app.run(debug=True)

#now reason will also be going to share that why the hypothesis is rejected and why accepted

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import joblib
# import os
# import pandas as pd
# import numpy as np

# app = Flask(__name__)
# CORS(app)

# # -------------------------------------------------
# # PATHS
# # -------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MODEL_DIR = os.path.join(BASE_DIR, "model")
# DATA_DIR = os.path.join(BASE_DIR, "data")

# # -------------------------------------------------
# # LOAD ML
# # -------------------------------------------------
# model = joblib.load(os.path.join(MODEL_DIR, "random_forest_large_smote.pkl"))
# vectorizer = joblib.load(os.path.join(MODEL_DIR, "tfidf_large_smote.pkl"))

# # -------------------------------------------------
# # LOAD CSVs
# # -------------------------------------------------
# disease_category_df = pd.read_csv(os.path.join(DATA_DIR, "ayurveda_large.csv"))
# templates_df = pd.read_csv(os.path.join(DATA_DIR, "ayurveda_templates.csv"))

# disease_category_df["disease"] = disease_category_df["disease"].str.strip()
# disease_category_df["category"] = disease_category_df["category"].str.strip()
# templates_df["disease"] = templates_df["disease"].str.strip()

# # -------------------------------------------------
# HIGH_CONF = 80
# REJECT_THRESHOLD = 2
# # -------------------------------------------------

# GENERIC_QUESTIONS = [
#     {"id": "chronic", "question": "Kya ye problem kaafi time se chal rahi hai?"},
#     {"id": "fatigue", "question": "Kya aapko roz thakan mehsoos hoti hai?"},
#     {"id": "progressive", "question": "Kya symptoms dheere-dheere badhte ja rahe hain?"}
# ]

# # -------------------------------------------------
# def calculate_confidence(prob):
#     return int(prob * 100)

# def update_confidence(base, answers):
#     boost = sum(5 for v in answers.values() if v.lower() == "yes")
#     return min(base + boost, 95)

# def count_negative_answers(answers):
#     return sum(1 for v in answers.values() if v.lower() == "no")

# def get_category(disease):
#     row = disease_category_df[disease_category_df["disease"] == disease]
#     return None if row.empty else row.iloc[0]["category"]

# def get_ayurveda(disease, body_type):
#     body_type = body_type.lower()

#     row = templates_df[templates_df["disease"] == disease]
#     if row.empty:
#         category = get_category(disease)
#         row = templates_df[templates_df["category"] == category]

#     if row.empty:
#         return {
#             "herbs": "Guduchi, Triphala",
#             "therapy": "Abhyanga, Panchakarma",
#             "diet": "Light, warm, sattvic diet",
#             "body_type_effect": "Helps balance doshas"
#         }

#     row = row.iloc[0]
#     effect = row.get(f"{body_type}_effect", "Balances dosha")

#     return {
#         "herbs": row["herbs"],
#         "therapy": row["therapy"],
#         "diet": row["diet"],
#         "body_type_effect": effect
#     }

# def generate_confidence_explanation(symptoms, rejected_disease, alternative_disease):
#     symptom_list = [s.strip() for s in symptoms.split(",")]

#     return {
#         "symptom_match": symptom_list[:2],
#         "why_previous_rejected": f"{rejected_disease} ke expected confirmation symptoms user ke answers se match nahi hue",
#         "model_reasoning": f"{alternative_disease} ML model ke ranking me next highest probability par tha"
#     }

# # -------------------------------------------------
# @app.route("/")
# def home():
#     return {"message": "Arogya AI Backend Running"}

# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.json

#     symptoms = data.get("symptoms", "")
#     body_type = data.get("body_type", "vata")
#     answers = data.get("answers")
#     locked_disease = data.get("locked_disease")

#     # ---------------------------
#     # FIRST CALL
#     # ---------------------------
#     if not locked_disease:
#         X = vectorizer.transform([symptoms])
#         probs = model.predict_proba(X)[0]

#         top_indices = np.argsort(probs)[::-1]
#         primary_idx = top_indices[0]
#         secondary_idx = top_indices[1]

#         disease = model.classes_[primary_idx]
#         alt_disease = model.classes_[secondary_idx]

#         confidence = calculate_confidence(probs[primary_idx])

#         if confidence < HIGH_CONF:
#             return jsonify({
#                 "status": "need_clarification",
#                 "predicted_disease": disease,
#                 "confidence": confidence,
#                 "questions": GENERIC_QUESTIONS,
#                 "alternative_candidate": alt_disease
#             })
#     else:
#         disease = locked_disease
#         confidence = 60

#     # ---------------------------
#     # CONTRADICTION HANDLING
#     # ---------------------------
#     if answers:
#         negative_count = count_negative_answers(answers)

#         if negative_count >= REJECT_THRESHOLD:
#             X = vectorizer.transform([symptoms])
#             probs = model.predict_proba(X)[0]
#             top_indices = np.argsort(probs)[::-1]

#             alt_disease = model.classes_[top_indices[1]]
#             alt_ayurveda = get_ayurveda(alt_disease, body_type)

#             explanation = generate_confidence_explanation(
#                 symptoms,
#                 disease,
#                 alt_disease
#             )

#             return jsonify({
#                 "status": "alternative_suggested",
#                 "rejected_disease": disease,
#                 "alternative_disease": alt_disease,
#                 "ayurveda": alt_ayurveda,
#                 "confidence_explanation": explanation,
#                 "message": "Pehli diagnosis match nahi hui. Alternative condition explainable reasoning ke saath suggest ki ja rahi hai.",
#                 "disclaimer": "Educational & research use only. Consult a healthcare professional."
#             })

#         confidence = update_confidence(confidence, answers)

#     # ---------------------------
#     ayurveda = get_ayurveda(disease, body_type)

#     return jsonify({
#         "status": "final",
#         "predicted_disease": disease,
#         "confidence": "High" if confidence >= HIGH_CONF else "Medium",
#         "ayurveda": ayurveda,
#         "disclaimer": "Educational & research use only. Consult a healthcare professional."
#     })

# # -------------------------------------------------
# if __name__ == "__main__":
#     app.run(debug=True)

## now added llm key so that it can generate better explanation using llm

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import joblib
# import os
# import pandas as pd
# import numpy as np
# import requests

# app = Flask(__name__)
# CORS(app)

# # -------------------------------------------------
# # PATHS
# # -------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MODEL_DIR = os.path.join(BASE_DIR, "model")
# DATA_DIR = os.path.join(BASE_DIR, "data")

# # -------------------------------------------------
# # LOAD ML
# # -------------------------------------------------
# model = joblib.load(os.path.join(MODEL_DIR, "random_forest_large_smote.pkl"))
# vectorizer = joblib.load(os.path.join(MODEL_DIR, "tfidf_large_smote.pkl"))

# # -------------------------------------------------
# # LOAD CSVs
# # -------------------------------------------------
# disease_category_df = pd.read_csv(os.path.join(DATA_DIR, "ayurveda_large.csv"))
# templates_df = pd.read_csv(os.path.join(DATA_DIR, "ayurveda_templates.csv"))

# disease_category_df["disease"] = disease_category_df["disease"].str.strip()
# disease_category_df["category"] = disease_category_df["category"].str.strip()
# templates_df["disease"] = templates_df["disease"].str.strip()

# # -------------------------------------------------
# # CONFIG
# # -------------------------------------------------
# HIGH_CONF = 80
# REJECT_THRESHOLD = 2
# OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

# GENERIC_QUESTIONS = [
#     {"id": "chronic", "question": "Kya ye problem kaafi time se chal rahi hai?"},
#     {"id": "fatigue", "question": "Kya aapko roz thakan mehsoos hoti hai?"},
#     {"id": "progressive", "question": "Kya symptoms dheere-dheere badhte ja rahe hain?"}
# ]

# # -------------------------------------------------
# # HELPER FUNCTIONS
# # -------------------------------------------------
# def calculate_confidence(prob):
#     return int(prob * 100)

# def update_confidence(base, answers):
#     boost = sum(5 for v in answers.values() if v.lower() == "yes")
#     return min(base + boost, 95)

# def count_negative_answers(answers):
#     return sum(1 for v in answers.values() if v.lower() == "no")

# def get_category(disease):
#     row = disease_category_df[disease_category_df["disease"] == disease]
#     return None if row.empty else row.iloc[0]["category"]

# def get_ayurveda(disease, body_type):
#     body_type = body_type.lower()
#     row = templates_df[templates_df["disease"] == disease]

#     if row.empty:
#         category = get_category(disease)
#         row = templates_df[templates_df["category"] == category]

#     if row.empty:
#         return {
#             "herbs": "Guduchi, Triphala",
#             "therapy": "Abhyanga, Panchakarma",
#             "diet": "Light, warm, sattvic diet",
#             "body_type_effect": "Helps balance doshas"
#         }

#     row = row.iloc[0]
#     return {
#         "herbs": row["herbs"],
#         "therapy": row["therapy"],
#         "diet": row["diet"],
#         "body_type_effect": row.get(f"{body_type}_effect", "Balances dosha")
#     }

# def generate_rule_explanation(symptoms, rejected, alternative):
#     symptom_list = [s.strip() for s in symptoms.split(",")]
#     return {
#         "symptom_match": symptom_list[:2],
#         "why_previous_rejected": f"{rejected} ke confirmation symptoms match nahi hue",
#         "model_reasoning": f"{alternative} ML model ke next highest probability par tha"
#     }

# # -------------------------------------------------
# # LLM EXPLANATION (SAFE LAYER)
# # -------------------------------------------------
# def generate_llm_explanation(disease, symptoms, ayurveda):
#     if not OPENROUTER_KEY:
#         return None

#     prompt = f"""
# You are a medical explanation assistant.
# Do NOT diagnose or give medical advice.

# Disease: {disease}
# Symptoms: {symptoms}

# Ayurvedic Herbs: {ayurveda['herbs']}
# Therapy: {ayurveda['therapy']}
# Diet: {ayurveda['diet']}

# Explain in simple, friendly Hinglish:
# - Why this condition matches symptoms
# - How Ayurveda helps in general terms
# """

#     try:
#         response = requests.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             headers={
#                 "Authorization": f"Bearer {OPENROUTER_KEY}",
#                 "Content-Type": "application/json"
#             },
#             json={
#                 "model": "mistralai/mistral-7b-instruct",
#                 "messages": [{"role": "user", "content": prompt}],
#                 "temperature": 0.3
#             },
#             timeout=10
#         )

#         return response.json()["choices"][0]["message"]["content"]

#     except Exception:
#         return None

# # -------------------------------------------------
# # ROUTES
# # -------------------------------------------------
# @app.route("/")
# def home():
#     return {"message": "Arogya AI Backend Running with LLM Plugin"}

# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.json

#     symptoms = data.get("symptoms", "")
#     body_type = data.get("body_type", "vata")
#     answers = data.get("answers")
#     locked_disease = data.get("locked_disease")

#     # FIRST CALL
#     if not locked_disease:
#         X = vectorizer.transform([symptoms])
#         probs = model.predict_proba(X)[0]
#         top = np.argsort(probs)[::-1]

#         disease = model.classes_[top[0]]
#         alt_disease = model.classes_[top[1]]
#         confidence = calculate_confidence(probs[top[0]])

#         if confidence < HIGH_CONF:
#             return jsonify({
#                 "status": "need_clarification",
#                 "predicted_disease": disease,
#                 "confidence": confidence,
#                 "questions": GENERIC_QUESTIONS
#             })
#     else:
#         disease = locked_disease
#         confidence = 60

#     # CONTRADICTION
#     if answers and count_negative_answers(answers) >= REJECT_THRESHOLD:
#         X = vectorizer.transform([symptoms])
#         probs = model.predict_proba(X)[0]
#         alt_disease = model.classes_[np.argsort(probs)[::-1][1]]

#         ayurveda = get_ayurveda(alt_disease, body_type)
#         rule_exp = generate_rule_explanation(symptoms, disease, alt_disease)
#         llm_exp = generate_llm_explanation(alt_disease, symptoms, ayurveda)

#         return jsonify({
#             "status": "alternative_suggested",
#             "rejected_disease": disease,
#             "alternative_disease": alt_disease,
#             "ayurveda": ayurveda,
#             "confidence_explanation": rule_exp,
#             "llm_explanation": llm_exp,
#             "disclaimer": "Educational & research use only. Consult a healthcare professional."
#         })

#     # FINAL
#     ayurveda = get_ayurveda(disease, body_type)
#     llm_exp = generate_llm_explanation(disease, symptoms, ayurveda)

#     return jsonify({
#         "status": "final",
#         "predicted_disease": disease,
#         "confidence": "High" if confidence >= HIGH_CONF else "Medium",
#         "ayurveda": ayurveda,
#         "llm_explanation": llm_exp,
#         "disclaimer": "Educational & research use only. Consult a healthcare professional."
#     })

# # -------------------------------------------------
# if __name__ == "__main__":
#     app.run(debug=True)

#################now the llm will ask smart questions based on symptoms if ml said m not sure ####################
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import joblib
# import os
# import pandas as pd
# import numpy as np
# import requests

# app = Flask(__name__)
# CORS(app)

# # -------------------------------------------------
# # PATHS
# # -------------------------------------------------
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MODEL_DIR = os.path.join(BASE_DIR, "model")
# DATA_DIR = os.path.join(BASE_DIR, "data")

# # -------------------------------------------------
# # LOAD ML
# # -------------------------------------------------
# model = joblib.load(os.path.join(MODEL_DIR, "random_forest_large_smote.pkl"))
# vectorizer = joblib.load(os.path.join(MODEL_DIR, "tfidf_large_smote.pkl"))

# # -------------------------------------------------
# # LOAD CSVs
# # -------------------------------------------------
# disease_category_df = pd.read_csv(os.path.join(DATA_DIR, "ayurveda_large.csv"))
# templates_df = pd.read_csv(os.path.join(DATA_DIR, "ayurveda_templates.csv"))

# disease_category_df["disease"] = disease_category_df["disease"].str.strip()
# disease_category_df["category"] = disease_category_df["category"].str.strip()
# templates_df["disease"] = templates_df["disease"].str.strip()

# # -------------------------------------------------
# # CONFIG
# # -------------------------------------------------
# HIGH_CONF = 80
# REJECT_THRESHOLD = 2
# OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

# FALLBACK_QUESTIONS = [
#     {"id": "chronic", "question": "Kya ye problem kaafi time se chal rahi hai?"},
#     {"id": "pain", "question": "Kya is problem ke saath pain hota hai?"},
#     {"id": "progressive", "question": "Kya symptoms dheere-dheere badhte ja rahe hain?"}
# ]

# # -------------------------------------------------
# # HELPER FUNCTIONS
# # -------------------------------------------------
# def calculate_confidence(prob):
#     return int(prob * 100)

# def count_negative_answers(answers):
#     return sum(1 for v in answers.values() if v.lower() == "no")

# def get_category(disease):
#     row = disease_category_df[disease_category_df["disease"] == disease]
#     return None if row.empty else row.iloc[0]["category"]

# def get_ayurveda(disease, body_type):
#     body_type = body_type.lower()
#     row = templates_df[templates_df["disease"] == disease]

#     if row.empty:
#         category = get_category(disease)
#         row = templates_df[templates_df["category"] == category]

#     if row.empty:
#         return {
#             "herbs": "Guduchi, Triphala",
#             "therapy": "Abhyanga, Panchakarma",
#             "diet": "Light, warm, sattvic diet",
#             "body_type_effect": "Helps balance doshas"
#         }

#     row = row.iloc[0]
#     return {
#         "herbs": row["herbs"],
#         "therapy": row["therapy"],
#         "diet": row["diet"],
#         "body_type_effect": row.get(f"{body_type}_effect", "Balances dosha")
#     }

# # -------------------------------------------------
# # SMART LLM QUESTIONS
# # -------------------------------------------------
# def generate_smart_questions(disease, symptoms):
#     if not OPENROUTER_KEY:
#         return FALLBACK_QUESTIONS

#     prompt = f"""
# You are a medical assistant.
# Do NOT diagnose or give treatment.
# Your task is to suggest 2–3 yes/no clarification questions.

# Disease hypothesis: {disease}
# User symptoms: {symptoms}

# Rules:
# - Only yes/no questions
# - Keep questions short
# - No medical advice
# - Output as numbered list
# """

#     try:
#         response = requests.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             headers={
#                 "Authorization": f"Bearer {OPENROUTER_KEY}",
#                 "Content-Type": "application/json"
#             },
#             json={
#                 "model": "mistralai/mistral-7b-instruct",
#                 "messages": [{"role": "user", "content": prompt}],
#                 "temperature": 0.2
#             },
#             timeout=10
#         )

#         text = response.json()["choices"][0]["message"]["content"]
#         lines = [l.strip("- ").strip() for l in text.split("\n") if l.strip()]
#         questions = []

#         for i, q in enumerate(lines[:3]):
#             questions.append({
#                 "id": f"q{i+1}",
#                 "question": q
#             })

#         return questions if questions else FALLBACK_QUESTIONS

#     except Exception:
#         return FALLBACK_QUESTIONS

# # -------------------------------------------------
# # ROUTES
# # -------------------------------------------------
# @app.route("/")
# def home():
#     return {"message": "Arogya AI Backend Running with Smart LLM Questions"}

# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.json

#     symptoms = data.get("symptoms", "")
#     body_type = data.get("body_type", "vata")
#     answers = data.get("answers")
#     locked_disease = data.get("locked_disease")

#     # ---------------- FIRST CALL ----------------
#     if not locked_disease:
#         X = vectorizer.transform([symptoms])
#         probs = model.predict_proba(X)[0]
#         top = np.argsort(probs)[::-1]

#         disease = model.classes_[top[0]]
#         confidence = calculate_confidence(probs[top[0]])

#         if confidence < HIGH_CONF:
#             smart_qs = generate_smart_questions(disease, symptoms)
#             return jsonify({
#                 "status": "need_clarification",
#                 "predicted_disease": disease,
#                 "confidence": confidence,
#                 "questions": smart_qs
#             })
#     else:
#         disease = locked_disease

#     # ---------------- CONTRADICTION ----------------
#     if answers and count_negative_answers(answers) >= REJECT_THRESHOLD:
#         X = vectorizer.transform([symptoms])
#         probs = model.predict_proba(X)[0]
#         alt_disease = model.classes_[np.argsort(probs)[::-1][1]]

#         ayurveda = get_ayurveda(alt_disease, body_type)

#         return jsonify({
#             "status": "alternative_suggested",
#             "rejected_disease": disease,
#             "alternative_disease": alt_disease,
#             "ayurveda": ayurveda,
#             "disclaimer": "Educational & research use only. Consult a healthcare professional."
#         })

#     # ---------------- FINAL ----------------
#     ayurveda = get_ayurveda(disease, body_type)

#     return jsonify({
#         "status": "final",
#         "predicted_disease": disease,
#         "confidence": "Medium",
#         "ayurveda": ayurveda,
#         "disclaimer": "Educational & research use only. Consult a healthcare professional."
#     })

# # -------------------------------------------------
# if __name__ == "__main__":
#     app.run(debug=True)

########################################################################################
#ML + Ayurveda logic same rahega
#Ye sirf agentic question controller hai
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import re

# app = Flask(__name__)
# CORS(app)

# # In-memory session (single user demo)
# SESSION = {}

# def reset_session():
#     SESSION.clear()
#     SESSION.update({
#         "disease": None,
#         "questions": [],
#         "index": 0,
#         "answers": []
#     })

# def clean_text(text):
#     return re.sub(r"<.*?>", "", text).strip()

# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.json or {}

#     symptoms = data.get("symptoms")
#     answer = data.get("answer")

#     # 🔴 CASE 1: NEW CONSULTATION (symptoms present)
#     if symptoms:
#         reset_session()

#         # ---- Normally ML + LLM logic yahan hota ----
#         SESSION["disease"] = "HPV"
#         SESSION["questions"] = [
#             "Have you noticed any genital warts or abnormal growths?",
#             "Have you experienced abnormal bleeding or discharge?",
#             "Have you recently been sexually active with a new partner?"
#         ]
#         SESSION["index"] = 0

#         return jsonify({
#             "status": "need_clarification",
#             "predicted_disease": SESSION["disease"],
#             "question": clean_text(SESSION["questions"][0]),
#             "confidence": 15
#         })

#     # 🔴 CASE 2: ANSWER TO QUESTION
#     if answer is not None:
#         SESSION["answers"].append(answer)
#         SESSION["index"] += 1

#         # Next question
#         if SESSION["index"] < len(SESSION["questions"]):
#             return jsonify({
#                 "status": "need_clarification",
#                 "predicted_disease": SESSION["disease"],
#                 "question": clean_text(
#                     SESSION["questions"][SESSION["index"]]
#                 ),
#                 "confidence": 15 - SESSION["index"] * 2
#             })

#         # Final decision
#         yes_count = SESSION["answers"].count("yes")

#         if yes_count == 0:
#             reset_session()
#             return jsonify({
#                 "status": "alternative_suggested",
#                 "rejected_disease": "HPV",
#                 "alternative_disease": "Hydrocele",
#                 "message": "Diagnosis rejected based on answers"
#             })

#         reset_session()
#         return jsonify({
#             "status": "final",
#             "predicted_disease": "HPV",
#             "confidence": "Medium"
#         })

#     return jsonify({"error": "Invalid request"}), 400

# if __name__ == "__main__":
#     reset_session()
#     app.run(debug=True)



########################### now uuid for each user will be there ###########################

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import uuid
# import re

# app = Flask(__name__)
# CORS(app)

# # 🔹 Multiple user sessions
# SESSIONS = {}

# def clean_text(text):
#     return re.sub(r"<.*?>", "", text).strip()

# def create_session():
#     return {
#         "disease": None,
#         "questions": [],
#         "index": 0,
#         "answers": []
#     }

# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.json or {}
#     session_id = data.get("session_id")

#     # 🔹 If no session_id → create new
#     if not session_id or session_id not in SESSIONS:
#         session_id = str(uuid.uuid4())
#         SESSIONS[session_id] = create_session()

#     session = SESSIONS[session_id]

#     symptoms = data.get("symptoms")
#     answer = data.get("answer")

#     # 🟢 NEW CONSULTATION
#     if symptoms:
#         SESSIONS[session_id] = create_session()
#         session = SESSIONS[session_id]

#         # (ML + LLM logic yahan aayega)
#         session["disease"] = "HPV"
#         session["questions"] = [
#             "Have you noticed any genital warts or abnormal growths?",
#             "Have you experienced abnormal bleeding or discharge?",
#             "Have you recently been sexually active with a new partner?"
#         ]
#         session["index"] = 0

#         return jsonify({
#             "session_id": session_id,
#             "status": "need_clarification",
#             "predicted_disease": session["disease"],
#             "question": clean_text(session["questions"][0]),
#             "confidence": 15
#         })

#     # 🟢 ANSWER FLOW
#     if answer is not None:
#         session["answers"].append(answer)
#         session["index"] += 1

#         if session["index"] < len(session["questions"]):
#             return jsonify({
#                 "session_id": session_id,
#                 "status": "need_clarification",
#                 "predicted_disease": session["disease"],
#                 "question": clean_text(
#                     session["questions"][session["index"]]
#                 ),
#                 "confidence": 15 - session["index"] * 2
#             })

#         # 🟢 FINAL DECISION
#         yes_count = session["answers"].count("yes")

#         if yes_count == 0:
#             del SESSIONS[session_id]
#             return jsonify({
#                 "session_id": session_id,
#                 "status": "alternative_suggested",
#                 "rejected_disease": "HPV",
#                 "alternative_disease": "Hydrocele",
#                 "message": "Diagnosis rejected based on answers"
#             })

#         del SESSIONS[session_id]
#         return jsonify({
#             "session_id": session_id,
#             "status": "final",
#             "predicted_disease": "HPV",
#             "confidence": "Medium"
#         })

#     return jsonify({"error": "Invalid request"}), 400

# if __name__ == "__main__":
#     app.run(debug=True)

############now auto cancel if user in active #################

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import uuid
# import time
# import re

# app = Flask(__name__)
# CORS(app)

# # ===== CONFIG =====
# SESSION_TIMEOUT = 300  # 5 minutes

# # ===== MEMORY STORE =====
# SESSIONS = {}

# def clean_text(text):
#     return re.sub(r"<.*?>", "", text).strip()

# def create_session():
#     return {
#         "disease": None,
#         "questions": [],
#         "answers": [],
#         "index": 0,
#         "memory": {},
#         "last_active": time.time()
#     }

# def cleanup_sessions():
#     now = time.time()
#     expired = [
#         sid for sid, s in SESSIONS.items()
#         if now - s["last_active"] > SESSION_TIMEOUT
#     ]
#     for sid in expired:
#         del SESSIONS[sid]

# @app.route("/predict", methods=["POST"])
# def predict():
#     cleanup_sessions()

#     data = request.json or {}
#     session_id = data.get("session_id")
#     symptoms = data.get("symptoms")
#     answer = data.get("answer")

#     # ===== CREATE SESSION =====
#     if not session_id or session_id not in SESSIONS:
#         session_id = str(uuid.uuid4())
#         SESSIONS[session_id] = create_session()

#     session = SESSIONS[session_id]
#     session["last_active"] = time.time()

#     # ===== NEW CONSULTATION =====
#     if symptoms:
#         SESSIONS[session_id] = create_session()
#         session = SESSIONS[session_id]

#         session["memory"]["initial_symptoms"] = symptoms
#         session["disease"] = "HPV"
#         session["questions"] = [
#             "Have you noticed any genital warts or abnormal growths?",
#             "Have you experienced abnormal bleeding or discharge?",
#             "Have you recently been sexually active with a new partner?"
#         ]

#         return jsonify({
#             "session_id": session_id,
#             "status": "need_clarification",
#             "predicted_disease": session["disease"],
#             "question": clean_text(session["questions"][0]),
#             "confidence": 15
#         })

#     # ===== ANSWER HANDLING =====
#     if answer is not None:
#         session["answers"].append(answer)
#         session["index"] += 1
#         session["memory"][f"answer_{session['index']}"] = answer

#         if session["index"] < len(session["questions"]):
#             return jsonify({
#                 "session_id": session_id,
#                 "status": "need_clarification",
#                 "predicted_disease": session["disease"],
#                 "question": clean_text(
#                     session["questions"][session["index"]]
#                 ),
#                 "confidence": 15 - session["index"] * 2
#             })

#         yes_count = session["answers"].count("yes")

#         if yes_count == 0:
#             summary = session["memory"]
#             del SESSIONS[session_id]
#             return jsonify({
#                 "status": "alternative_suggested",
#                 "rejected_disease": "HPV",
#                 "alternative_disease": "Hydrocele",
#                 "reasoning_memory": summary
#             })

#         summary = session["memory"]
#         del SESSIONS[session_id]
#         return jsonify({
#             "status": "final",
#             "predicted_disease": "HPV",
#             "confidence": "Medium",
#             "reasoning_memory": summary
#         })

#     return jsonify({"error": "Invalid request"}), 400

# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import uuid
# import time
# import os
# import joblib
# import re
# import numpy as np

# # ===================== BASIC SETUP =====================
# app = Flask(__name__)
# CORS(app)

# SESSION_TIMEOUT = 300  # 5 minutes
# SESSIONS = {}

# # ===================== SAFE PATH SETUP =====================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MODEL_PATH = os.path.join(
#     BASE_DIR, "..", "model", "random_forest_large_smote.pkl"
# )
# VECTORIZER_PATH = os.path.join(
#     BASE_DIR, "..", "model", "tfidf_large_smote.pkl"
# )

# print("Loading ML model from:", MODEL_PATH)
# print("Loading vectorizer from:", VECTORIZER_PATH)

# model = joblib.load(MODEL_PATH)
# vectorizer = joblib.load(VECTORIZER_PATH)

# # ===================== QUESTION BANK =====================
# QUESTION_BANK = {
#     "HPV": [
#         "Have you noticed any genital warts or abnormal growths?",
#         "Have you experienced abnormal bleeding or discharge?",
#         "Have you recently been sexually active with a new partner?"
#     ],
#     "Epididymitis": [
#         "Do you feel pain in the scrotum?",
#         "Have you had fever recently?",
#         "Is there swelling or tenderness in the testicular area?"
#     ],
#     "Hypothyroidism": [
#         "Do you often feel unusually cold?",
#         "Have you gained weight recently?",
#         "Do you feel tired most of the time?"
#     ],
#     "Diabetes": [
#         "Do you feel excessive thirst?",
#         "Are you urinating frequently?",
#         "Do you feel sudden fatigue?"
#     ]
# }

# # ===================== UTILS =====================
# def clean_text(text):
#     return re.sub(r"<.*?>", "", text).strip()

# def new_session():
#     return {
#         "disease": None,
#         "questions": [],
#         "answers": [],
#         "q_index": 0,
#         "confidence": None,
#         "created_at": time.time()
#     }

# def cleanup_sessions():
#     now = time.time()
#     expired = [
#         sid for sid, s in SESSIONS.items()
#         if now - s["created_at"] > SESSION_TIMEOUT
#     ]
#     for sid in expired:
#         del SESSIONS[sid]

# def ml_predict(symptoms):
#     X = vectorizer.transform([symptoms])
#     probs = model.predict_proba(X)[0]
#     classes = model.classes_
#     idx = int(np.argmax(probs))
#     return classes[idx], round(float(probs[idx]) * 100, 2)

# # ===================== MAIN API =====================
# @app.route("/predict", methods=["POST"])
# def predict():
#     cleanup_sessions()
#     data = request.json or {}

#     session_id = data.get("session_id")
#     symptoms = data.get("symptoms")
#     answer = data.get("answer")

#     # ---------- SESSION INIT ----------
#     if not session_id or session_id not in SESSIONS:
#         session_id = str(uuid.uuid4())
#         SESSIONS[session_id] = new_session()

#     session = SESSIONS[session_id]

#     # ---------- NEW CONSULT ----------
#     if symptoms:
#         disease, confidence = ml_predict(symptoms)

#         session["disease"] = disease
#         session["confidence"] = confidence
#         session["questions"] = QUESTION_BANK.get(
#             disease,
#             [
#                 "Are your symptoms persistent?",
#                 "Do symptoms worsen over time?",
#                 "Do they affect daily activities?"
#             ]
#         )
#         session["q_index"] = 0
#         session["answers"] = []

#         return jsonify({
#             "session_id": session_id,
#             "status": "need_clarification",
#             "predicted_disease": disease,
#             "confidence": confidence,
#             "question": clean_text(session["questions"][0])
#         })

#     # ---------- ANSWER FLOW ----------
#     if answer is not None:
#         session["answers"].append(answer.lower())
#         session["q_index"] += 1

#         if session["q_index"] < len(session["questions"]):
#             return jsonify({
#                 "session_id": session_id,
#                 "status": "need_clarification",
#                 "predicted_disease": session["disease"],
#                 "confidence": session["confidence"],
#                 "question": clean_text(
#                     session["questions"][session["q_index"]]
#                 )
#             })

#         yes_count = session["answers"].count("yes")
#         disease = session["disease"]
#         confidence = session["confidence"]

#         del SESSIONS[session_id]

#         if yes_count == 0:
#             return jsonify({
#                 "status": "hypothesis_rejected",
#                 "message": "Aapke answers diagnosis ko support nahi karte",
#                 "suggestion": "Please consult a medical professional"
#             })

#         return jsonify({
#             "status": "final",
#             "predicted_disease": disease,
#             "confidence": confidence,
#             "disclaimer": "Educational & research use only. Consult a healthcare professional."
#         })

#     return jsonify({"error": "Invalid request"}), 400

# # ===================== RUN =====================
# if __name__ == "__main__":
#     app.run(debug=True)


### missed the auraveda part + llm question generation part ###

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import uuid, time, os, re
# import joblib
# import numpy as np
# import requests

# # ================= BASIC =================
# app = Flask(__name__)
# CORS(app)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "random_forest_large_smote.pkl")
# VECTORIZER_PATH = os.path.join(BASE_DIR, "..", "model", "tfidf_large_smote.pkl")

# model = joblib.load(MODEL_PATH)
# vectorizer = joblib.load(VECTORIZER_PATH)

# SESSION_TIMEOUT = 300
# SESSIONS = {}

# # ================= RULE QUESTIONS =================
# QUESTION_BANK = {
#     "HPV": [
#         "Have you noticed genital warts or abnormal growths?",
#         "Have you experienced abnormal bleeding or discharge?",
#         "Have you recently been sexually active with a new partner?"
#     ],
#     "Epididymitis": [
#         "Do you feel pain in the scrotum?",
#         "Is there swelling or tenderness in the testicular area?",
#         "Have you had fever recently?"
#     ],
#     "Hypothyroidism": [
#         "Do you feel unusually cold most of the time?",
#         "Have you gained weight recently?",
#         "Do you experience constant fatigue?"
#     ]
# }

# # ================= LLM CONFIG =================
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # optional

# def llm_generate_questions(disease, symptoms):
#     if not OPENROUTER_API_KEY:
#         return [
#             f"Can you describe how severe your {symptoms} are?",
#             "Are these symptoms getting worse with time?",
#             "Do these symptoms affect your daily routine?"
#         ]

#     prompt = f"""
# You are a doctor.
# Disease suspected: {disease}
# Symptoms: {symptoms}

# Ask ONLY 3 clear yes/no medical questions
# to confirm or reject this disease.
# """

#     res = requests.post(
#         "https://openrouter.ai/api/v1/chat/completions",
#         headers={
#             "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#             "Content-Type": "application/json"
#         },
#         json={
#             "model": "openai/gpt-3.5-turbo",
#             "messages": [{"role": "user", "content": prompt}]
#         },
#         timeout=15
#     )

#     text = res.json()["choices"][0]["message"]["content"]
#     questions = [q.strip("- ").strip() for q in text.split("\n") if "?" in q]
#     return questions[:3]

# # ================= HELPERS =================
# def cleanup_sessions():
#     now = time.time()
#     for sid in list(SESSIONS.keys()):
#         if now - SESSIONS[sid]["created"] > SESSION_TIMEOUT:
#             del SESSIONS[sid]

# def ml_predict(symptoms):
#     X = vectorizer.transform([symptoms])
#     probs = model.predict_proba(X)[0]
#     idx = np.argmax(probs)
#     return model.classes_[idx], round(float(probs[idx]) * 100, 2)

# # ================= API =================
# @app.route("/predict", methods=["POST"])
# def predict():
#     cleanup_sessions()
#     data = request.json or {}

#     session_id = data.get("session_id")
#     symptoms = data.get("symptoms")
#     answer = data.get("answer")

#     if not session_id or session_id not in SESSIONS:
#         session_id = str(uuid.uuid4())
#         SESSIONS[session_id] = {
#             "created": time.time(),
#             "disease": None,
#             "questions": [],
#             "answers": [],
#             "index": 0,
#             "confidence": None
#         }

#     session = SESSIONS[session_id]

#     # ===== START CONSULT =====
#     if symptoms:
#         disease, confidence = ml_predict(symptoms)
#         session["disease"] = disease
#         session["confidence"] = confidence

#         if disease in QUESTION_BANK:
#             session["questions"] = QUESTION_BANK[disease]
#         else:
#             session["questions"] = llm_generate_questions(disease, symptoms)

#         session["index"] = 0
#         session["answers"] = []

#         return jsonify({
#             "session_id": session_id,
#             "status": "need_clarification",
#             "predicted_disease": disease,
#             "confidence": confidence,
#             "question": session["questions"][0]
#         })

#     # ===== ANSWER FLOW =====
#     if answer:
#         session["answers"].append(answer.lower())
#         session["index"] += 1

#         if session["index"] < len(session["questions"]):
#             return jsonify({
#                 "session_id": session_id,
#                 "status": "need_clarification",
#                 "predicted_disease": session["disease"],
#                 "confidence": session["confidence"],
#                 "question": session["questions"][session["index"]]
#             })

#         yes_count = session["answers"].count("yes")
#         disease = session["disease"]
#         confidence = session["confidence"]
#         del SESSIONS[session_id]

#         if yes_count == 0:
#             return jsonify({
#                 "status": "hypothesis_rejected",
#                 "message": "Your answers do not support this diagnosis."
#             })

#         return jsonify({
#             "status": "final",
#             "predicted_disease": disease,
#             "confidence": confidence,
#             "disclaimer": "Educational & research use only."
#         })

#     return jsonify({"error": "Invalid request"}), 400

# # ================= RUN =================
# if __name__ == "__main__":
#     app.run(debug=True)

#### completing the ayurveda and llm question generation part ###

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import uuid, time, os, re
# import joblib
# import numpy as np
# import pandas as pd
# import requests

# # ================= BASIC SETUP =================
# app = Flask(__name__)
# CORS(app)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "random_forest_large_smote.pkl")
# VECTORIZER_PATH = os.path.join(BASE_DIR, "..", "model", "tfidf_large_smote.pkl")

# AYURVEDA_TEMPLATE_PATH = os.path.join(BASE_DIR, "..", "data", "ayurveda_templates.csv")

# model = joblib.load(MODEL_PATH)
# vectorizer = joblib.load(VECTORIZER_PATH)

# ayurveda_templates = pd.read_csv(AYURVEDA_TEMPLATE_PATH)

# SESSION_TIMEOUT = 300
# SESSIONS = {}

# # ================= RULE-BASED QUESTIONS =================
# QUESTION_BANK = {
#     "HPV": [
#         "Have you noticed genital warts or abnormal growths?",
#         "Have you experienced abnormal bleeding or discharge?",
#         "Have you recently been sexually active with a new partner?"
#     ],
#     "Epididymitis": [
#         "Do you feel pain in the scrotum?",
#         "Is there swelling or tenderness in the testicular area?",
#         "Have you had fever recently?"
#     ],
#     "Hypothyroidism": [
#         "Do you feel unusually cold most of the time?",
#         "Have you gained weight recently?",
#         "Do you experience constant fatigue?"
#     ]
# }

# # ================= LLM (QUESTIONS ONLY) =================
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# def llm_generate_questions(disease, symptoms):
#     if not OPENROUTER_API_KEY:
#         return [
#             f"Are your {symptoms} persistent?",
#             "Are symptoms worsening with time?",
#             "Do these symptoms affect daily activities?"
#         ]

#     prompt = f"""
# You are a medical doctor.
# Suspected disease: {disease}
# Symptoms: {symptoms}

# Ask exactly 3 yes/no diagnostic questions.
# """

#     res = requests.post(
#         "https://openrouter.ai/api/v1/chat/completions",
#         headers={
#             "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#             "Content-Type": "application/json"
#         },
#         json={
#             "model": "openai/gpt-3.5-turbo",
#             "messages": [{"role": "user", "content": prompt}]
#         },
#         timeout=15
#     )

#     text = res.json()["choices"][0]["message"]["content"]
#     return [q.strip("- ").strip() for q in text.split("\n") if "?" in q][:3]

# # ================= HELPERS =================
# def cleanup_sessions():
#     now = time.time()
#     for sid in list(SESSIONS.keys()):
#         if now - SESSIONS[sid]["created"] > SESSION_TIMEOUT:
#             del SESSIONS[sid]

# def ml_predict(symptoms):
#     X = vectorizer.transform([symptoms])
#     probs = model.predict_proba(X)[0]
#     idx = np.argmax(probs)
#     return model.classes_[idx], round(float(probs[idx]) * 100, 2)

# def get_ayurveda(disease, body_type="kapha"):
#     row = ayurveda_templates[ayurveda_templates["disease"] == disease]

#     if row.empty:
#         return {
#             "herbs": "Not specified",
#             "therapy": "Not specified",
#             "diet": "Not specified",
#             "body_type_effect": "General balance support"
#         }

#     row = row.iloc[0]

#     return {
#         "herbs": row["herbs"],
#         "therapy": row["therapy"],
#         "diet": row["diet"],
#         "body_type_effect": row.get(f"{body_type}_effect", "General balance support")
#     }

# # ================= API =================
# @app.route("/predict", methods=["POST"])
# def predict():
#     cleanup_sessions()
#     data = request.json or {}

#     session_id = data.get("session_id")
#     symptoms = data.get("symptoms")
#     answer = data.get("answer")
#     body_type = data.get("body_type", "kapha").lower()

#     if not session_id or session_id not in SESSIONS:
#         session_id = str(uuid.uuid4())
#         SESSIONS[session_id] = {
#             "created": time.time(),
#             "disease": None,
#             "questions": [],
#             "answers": [],
#             "index": 0,
#             "confidence": None
#         }

#     session = SESSIONS[session_id]

#     # ===== START CONSULT =====
#     if symptoms:
#         disease, confidence = ml_predict(symptoms)
#         session["disease"] = disease
#         session["confidence"] = confidence

#         if disease in QUESTION_BANK:
#             session["questions"] = QUESTION_BANK[disease]
#         else:
#             session["questions"] = llm_generate_questions(disease, symptoms)

#         session["index"] = 0
#         session["answers"] = []

#         return jsonify({
#             "session_id": session_id,
#             "status": "need_clarification",
#             "predicted_disease": disease,
#             "confidence": confidence,
#             "question": session["questions"][0]
#         })

#     # ===== ANSWER FLOW =====
#     if answer:
#         session["answers"].append(answer.lower())
#         session["index"] += 1

#         if session["index"] < len(session["questions"]):
#             return jsonify({
#                 "session_id": session_id,
#                 "status": "need_clarification",
#                 "predicted_disease": session["disease"],
#                 "confidence": session["confidence"],
#                 "question": session["questions"][session["index"]]
#             })

#         yes_count = session["answers"].count("yes")
#         disease = session["disease"]
#         confidence = session["confidence"]

#         del SESSIONS[session_id]

#         if yes_count == 0:
#             return jsonify({
#                 "status": "hypothesis_rejected",
#                 "message": "User answers do not support this diagnosis."
#             })

#         ayurveda = get_ayurveda(disease, body_type)

#         return jsonify({
#             "status": "final",
#             "predicted_disease": disease,
#             "confidence": confidence,
#             "ayurveda": ayurveda,
#             "disclaimer": "Educational & research use only. Consult a healthcare professional."
#         })

#     return jsonify({"error": "Invalid request"}), 400

# # ================= RUN =================
# if __name__ == "__main__":
#     app.run(debug=True)


########################################end #########################################

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import uuid
# import joblib
# import pandas as pd
# import os

# app = Flask(__name__)
# CORS(app)

# # ---------------- PATHS ----------------
# BASE_DIR = os.path.dirname(__file__)
# MODEL_DIR = os.path.join(BASE_DIR, "..", "model")
# DATA_DIR = os.path.join(BASE_DIR, "..", "data")

# MODEL_PATH = os.path.join(MODEL_DIR, "random_forest_large_smote.pkl")
# VECT_PATH = os.path.join(MODEL_DIR, "tfidf_large_smote.pkl")

# AYUR_LARGE = os.path.join(DATA_DIR, "ayurveda_large.csv")
# AYUR_TEMPLATES = os.path.join(DATA_DIR, "ayurveda_templates.csv")

# # ---------------- LOADS ----------------
# model = joblib.load(MODEL_PATH)
# vectorizer = joblib.load(VECT_PATH)

# ayur_large_df = pd.read_csv(AYUR_LARGE)
# ayur_templates_df = pd.read_csv(AYUR_TEMPLATES)

# # ---------------- MEMORY ----------------
# SESSIONS = {}

# # ---------------- HELPERS ----------------
# def get_ayurveda(disease, body_type="kapha"):
#     row = ayur_templates_df[
#         ayur_templates_df["disease"].str.lower() == disease.lower()
#     ]

#     if row.empty:
#         return {
#             "herbs": "Not specified",
#             "therapy": "Not specified",
#             "diet": "Not specified",
#             "body_type_effect": "Not specified"
#         }

#     return {
#         "herbs": row.iloc[0]["herbs"],
#         "therapy": row.iloc[0]["therapy"],
#         "diet": row.iloc[0]["diet"],
#         "body_type_effect": row.iloc[0][f"{body_type}_effect"]
#     }


# def smart_questions(disease):
#     QUESTION_BANK = {
#         "Gastritis": [
#             "Have you been experiencing frequent stomach pain?",
#             "Do you feel bloated after meals?",
#             "Have you experienced nausea or vomiting?"
#         ],
#         "HPV": [
#             "Have you noticed any genital warts or abnormal growths?",
#             "Any unusual discharge or bleeding?",
#             "Have you recently had a new sexual partner?"
#         ],
#         "Epididymitis": [
#             "Do you feel pain in the scrotum?",
#             "Any fever recently?",
#             "Any urinary discomfort?"
#         ]
#     }
#     return QUESTION_BANK.get(disease, [
#         "Are your symptoms persistent?",
#         "Are symptoms getting worse over time?",
#         "Do symptoms affect daily life?"
#     ])


# # ---------------- API ----------------
# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.json

#     # ---------- NEW SESSION ----------
#     if "symptoms" in data:
#         session_id = str(uuid.uuid4())
#         symptoms = data["symptoms"]

#         X = vectorizer.transform([symptoms])
#         probs = model.predict_proba(X)[0]
#         classes = model.classes_

#         ranked = sorted(
#             zip(classes, probs),
#             key=lambda x: x[1],
#             reverse=True
#         )

#         disease, confidence = ranked[0]

#         SESSIONS[session_id] = {
#             "disease": disease,
#             "confidence": confidence,
#             "ranked": ranked,
#             "q_index": 0,
#             "answers": []
#         }

#         return jsonify({
#             "session_id": session_id,
#             "predicted_disease": disease,
#             "confidence": int(confidence * 100),
#             "question": smart_questions(disease)[0],
#             "status": "need_clarification"
#         })

#     # ---------- FOLLOW UP ----------
#     session_id = data.get("session_id")
#     answer = data.get("answer", "").lower()

#     session = SESSIONS.get(session_id)
#     disease = session["disease"]
#     questions = smart_questions(disease)

#     session["answers"].append(answer)
#     session["q_index"] += 1

#     # ---------- ASK NEXT ----------
#     if session["q_index"] < len(questions):
#         return jsonify({
#             "question": questions[session["q_index"]],
#             "status": "need_clarification"
#         })

#     # ---------- CONFIRM / REJECT ----------
#     yes_count = sum(1 for a in session["answers"] if a.startswith("y"))

#     if yes_count < 2:
#         # reject hypothesis
#         alt = session["ranked"][1][0]

#         ayur = get_ayurveda(alt)

#         return jsonify({
#             "status": "alternative_suggested",
#             "rejected_disease": disease,
#             "alternative_disease": alt,
#             "ayurveda": ayur,
#             "confidence_explanation": {
#                 "symptom_match": ["fatigue", "swelling"],
#                 "why_previous_rejected": "Confirmation answers did not support initial disease",
#                 "model_reasoning": "Second highest ML probability"
#             },
#             "llm_explanation": (
#                 f"{alt} ek condition ho sakti hai kyunki symptoms aur ML pattern "
#                 "zyaada closely match kar rahe hain. Pehli disease ke required signs "
#                 "confirm nahi hue."
#             ),
#             "disclaimer": "Educational & research use only"
#         })

#     # ---------- FINAL ----------
#     ayur = get_ayurveda(disease)

#     return jsonify({
#         "status": "final",
#         "predicted_disease": disease,
#         "confidence": int(session["confidence"] * 100),
#         "ayurveda": ayur,
#         "confidence_explanation": {
#             "symptom_match": ["stomach pain", "bloating", "nausea"],
#             "model_reasoning": "High overlap with trained disease patterns",
#             "why_previous_rejected": None
#         },
#         "llm_explanation": (
#             f"{disease} ek aisi condition hai jisme digestive system "
#             "irritation hota hai. Aapke jawab is diagnosis ko support karte hain."
#         ),
#         "disclaimer": "Educational & research use only"
#     })


# if __name__ == "__main__":
#     app.run(debug=True)



# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import uuid
# import joblib
# import pandas as pd
# import os
# import requests

# app = Flask(__name__)
# CORS(app)

# # ---------------- PATHS ----------------
# BASE_DIR = os.path.dirname(__file__)
# MODEL_DIR = os.path.join(BASE_DIR, "..", "model")
# DATA_DIR = os.path.join(BASE_DIR, "..", "data")

# MODEL_PATH = os.path.join(MODEL_DIR, "random_forest_large_smote.pkl")
# VECT_PATH = os.path.join(MODEL_DIR, "tfidf_large_smote.pkl")

# AYUR_LARGE = os.path.join(DATA_DIR, "ayurveda_large.csv")
# AYUR_TEMPLATES = os.path.join(DATA_DIR, "ayurveda_templates.csv")

# # ---------------- LOAD ----------------
# model = joblib.load(MODEL_PATH)
# vectorizer = joblib.load(VECT_PATH)

# ayur_templates_df = pd.read_csv(AYUR_TEMPLATES)

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# SESSIONS = {}

# # ---------------- AYURVEDA ----------------
# def get_ayurveda(disease, body_type="kapha"):
#     row = ayur_templates_df[
#         ayur_templates_df["disease"].str.lower() == disease.lower()
#     ]

#     if row.empty:
#         return {
#             "herbs": "Not specified",
#             "therapy": "Not specified",
#             "diet": "Not specified",
#             "body_type_effect": "Not specified"
#         }

#     return {
#         "herbs": row.iloc[0]["herbs"],
#         "therapy": row.iloc[0]["therapy"],
#         "diet": row.iloc[0]["diet"],
#         "body_type_effect": row.iloc[0][f"{body_type}_effect"]
#     }

# # ---------------- FALLBACK QUESTIONS ----------------
# def fallback_questions():
#     return [
#         "Are your symptoms persistent?",
#         "Are the symptoms worsening over time?",
#         "Do symptoms interfere with daily activities?"
#     ]

# # ---------------- LLM QUESTION GENERATOR ----------------
# def llm_generate_questions(disease, symptoms):
#     try:
#         prompt = f"""
# You are a medical doctor.
# Generate exactly 3 diagnostic yes/no questions
# to confirm or reject the disease: {disease}

# Patient symptoms: {symptoms}

# Return only numbered questions.
# """

#         res = requests.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             headers={
#                 "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#                 "Content-Type": "application/json"
#             },
#             json={
#                 "model": "openai/gpt-4o-mini",
#                 "messages": [{"role": "user", "content": prompt}],
#                 "temperature": 0.4
#             },
#             timeout=15
#         )

#         text = res.json()["choices"][0]["message"]["content"]
#         questions = [q.strip() for q in text.split("\n") if "?" in q]

#         if len(questions) >= 3:
#             return questions[:3]

#     except Exception:
#         pass

#     return fallback_questions()

# # ---------------- API ----------------
# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.json

#     # -------- NEW SESSION --------
#     if "symptoms" in data:
#         session_id = str(uuid.uuid4())
#         symptoms = data["symptoms"]

#         X = vectorizer.transform([symptoms])
#         probs = model.predict_proba(X)[0]
#         classes = model.classes_

#         ranked = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)
#         disease, confidence = ranked[0]

#         questions = llm_generate_questions(disease, symptoms)

#         SESSIONS[session_id] = {
#             "disease": disease,
#             "confidence": confidence,
#             "ranked": ranked,
#             "questions": questions,
#             "q_index": 0,
#             "answers": [],
#             "symptoms": symptoms
#         }

#         return jsonify({
#             "session_id": session_id,
#             "predicted_disease": disease,
#             "confidence": int(confidence * 100),
#             "question": questions[0],
#             "status": "need_clarification"
#         })

#     # -------- FOLLOW UP --------
#     session_id = data.get("session_id")
#     answer = data.get("answer", "").lower()

#     session = SESSIONS.get(session_id)
#     session["answers"].append(answer)
#     session["q_index"] += 1

#     # -------- NEXT QUESTION --------
#     if session["q_index"] < len(session["questions"]):
#         return jsonify({
#             "question": session["questions"][session["q_index"]],
#             "status": "need_clarification"
#         })

#     # -------- CONFIRM / REJECT --------
#     yes_count = sum(1 for a in session["answers"] if a.startswith("y"))

#     if yes_count < 2:
#         alt = session["ranked"][1][0]
#         ayur = get_ayurveda(alt)

#         return jsonify({
#             "status": "alternative_suggested",
#             "rejected_disease": session["disease"],
#             "alternative_disease": alt,
#             "ayurveda": ayur,
#             "confidence_explanation": {
#                 "symptom_match": ["swelling", "fatigue"],
#                 "why_previous_rejected": "LLM confirmation questions not satisfied",
#                 "model_reasoning": "Next highest ML probability"
#             },
#             "llm_explanation": (
#                 f"{alt} zyada likely lag raha hai kyunki "
#                 "pehli disease ke confirmation signals match nahi hue."
#             ),
#             "disclaimer": "Educational & research use only"
#         })

#     # -------- FINAL --------
#     ayur = get_ayurveda(session["disease"])

#     return jsonify({
#         "status": "final",
#         "predicted_disease": session["disease"],
#         "confidence": int(session["confidence"] * 100),
#         "ayurveda": ayur,
#         "confidence_explanation": {
#             "symptom_match": session["symptoms"].split(","),
#             "model_reasoning": "LLM + ML agreement",
#             "why_previous_rejected": None
#         },
#         "llm_explanation": (
#             f"{session['disease']} ek condition hai jo aapke symptoms "
#             "aur LLM analysis dono se confirm hui."
#         ),
#         "disclaimer": "Educational & research use only"
#     })

# if __name__ == "__main__":
#     app.run(debug=True)




########### for all no fall back ########################

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import uuid
# import joblib
# import pandas as pd
# import os
# import requests

# app = Flask(__name__)
# CORS(app)

# @app.route("/")
# def home():
#     return "Arogya AI Backend Running"

# # ---------------- PATHS ----------------
# BASE_DIR = os.path.dirname(__file__)
# MODEL_DIR = os.path.join(BASE_DIR, "..", "model")
# DATA_DIR = os.path.join(BASE_DIR, "..", "data")

# MODEL_PATH = os.path.join(MODEL_DIR, "random_forest_large_smote.pkl")
# VECT_PATH = os.path.join(MODEL_DIR, "tfidf_large_smote.pkl")

# AYUR_LARGE = os.path.join(DATA_DIR, "ayurveda_large.csv")
# AYUR_TEMPLATES = os.path.join(DATA_DIR, "ayurveda_templates.csv")

# # ---------------- LOAD ----------------
# model = joblib.load(MODEL_PATH)
# vectorizer = joblib.load(VECT_PATH)

# ayur_templates_df = pd.read_csv(AYUR_TEMPLATES)

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# SESSIONS = {}

# # ---------------- AYURVEDA ----------------
# def get_ayurveda(disease, body_type="kapha"):
#     row = ayur_templates_df[
#         ayur_templates_df["disease"].str.lower() == disease.lower()
#     ]

#     if row.empty:
#         return {
#             "herbs": "Not specified",
#             "therapy": "Not specified",
#             "diet": "Not specified",
#             "body_type_effect": "Not specified"
#         }

#     return {
#         "herbs": row.iloc[0]["herbs"],
#         "therapy": row.iloc[0]["therapy"],
#         "diet": row.iloc[0]["diet"],
#         "body_type_effect": row.iloc[0][f"{body_type}_effect"]
#     }

# # ---------------- FALLBACK QUESTIONS ----------------
# def fallback_questions():
#     return [
#         "Are your symptoms persistent?",
#         "Are the symptoms worsening over time?",
#         "Do symptoms interfere with daily activities?"
#     ]

# # ---------------- LLM QUESTION GENERATOR ----------------
# def llm_generate_questions(disease, symptoms):
#     try:
#         prompt = f"""
# You are a medical doctor.
# Generate exactly 3 diagnostic yes/no questions
# to confirm or reject the disease: {disease}

# Patient symptoms: {symptoms}

# Return only numbered questions.
# """

#         res = requests.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             headers={
#                 "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#                 "Content-Type": "application/json"
#             },
#             json={
#                 "model": "openai/gpt-4o-mini",
#                 "messages": [{"role": "user", "content": prompt}],
#                 "temperature": 0.4
#             },
#             timeout=15
#         )

#         text = res.json()["choices"][0]["message"]["content"]
#         questions = [q.strip() for q in text.split("\n") if "?" in q]

#         if len(questions) >= 3:
#             return questions[:3]

#     except Exception:
#         pass

#     return fallback_questions()

# # ---------------- API ----------------
# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.json

#     # -------- NEW SESSION --------
#     if "symptoms" in data:
#         session_id = str(uuid.uuid4())
#         symptoms = data["symptoms"]

#         X = vectorizer.transform([symptoms])
#         probs = model.predict_proba(X)[0]
#         classes = model.classes_

#         ranked = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)
#         disease, confidence = ranked[0]

#         questions = llm_generate_questions(disease, symptoms)

#         SESSIONS[session_id] = {
#             "disease": disease,
#             "confidence": confidence,
#             "ranked": ranked,
#             "questions": questions,
#             "q_index": 0,
#             "answers": [],
#             "symptoms": symptoms,
#             "on_alternative": False
#         }

#         return jsonify({
#             "session_id": session_id,
#             "predicted_disease": disease,
#             "confidence": int(confidence * 100),
#             "question": questions[0],
#             "status": "need_clarification"
#         })

#     # -------- FOLLOW UP --------
#     session_id = data.get("session_id")
#     answer = data.get("answer", "").lower()

#     session = SESSIONS.get(session_id)

#     if not session:
#         return jsonify({"error": "Session not found. Please start again."}), 400

#     session["answers"].append(answer)
#     session["q_index"] += 1

#     # -------- NEXT QUESTION --------
#     if session["q_index"] < len(session["questions"]):
#         return jsonify({
#             "session_id": session_id,
#             "question": session["questions"][session["q_index"]],
#             "status": "need_clarification"
#         })

#     # -------- CONFIRM / REJECT --------
#     yes_count = sum(1 for a in session["answers"] if a.startswith("y"))

#     if yes_count < 2:

#         # --- Already tried alternative too → give up gracefully ---
#         if session.get("on_alternative"):
#             alt = session["disease"]
#             ayur = get_ayurveda(alt)
#             return jsonify({
#                 "status": "final",
#                 "predicted_disease": alt,
#                 "confidence": int(session["confidence"] * 100),
#                 "ayurveda": ayur,
#                 "confidence_explanation": {
#                     "symptom_match": session["symptoms"].split(","),
#                     "model_reasoning": "Best match after ruling out primary hypothesis",
#                     "why_previous_rejected": "Confirmation questions not satisfied for primary disease"
#                 },
#                 "llm_explanation": (
#                     f"Your symptoms most closely match {alt}, though confirmation "
#                     "was inconclusive. Please consult a doctor for an accurate diagnosis."
#                 ),
#                 "disclaimer": "Educational & research use only"
#             })

#         # --- First rejection → switch to 2nd ranked disease ---
#         alt_disease = session["ranked"][1][0]
#         alt_confidence = session["ranked"][1][1]
#         new_questions = llm_generate_questions(alt_disease, session["symptoms"])

#         # Update session in place
#         session["disease"] = alt_disease
#         session["confidence"] = alt_confidence
#         session["questions"] = new_questions
#         session["q_index"] = 0
#         session["answers"] = []
#         session["on_alternative"] = True

#         return jsonify({
#             "session_id": session_id,
#             "predicted_disease": alt_disease,
#             "status": "need_clarification",
#             "question": new_questions[0],
#             "message": f"Ruling out first hypothesis. Let me check for {alt_disease} instead."
#         })

#     # -------- FINAL --------
#     ayur = get_ayurveda(session["disease"])

#     return jsonify({
#         "status": "final",
#         "predicted_disease": session["disease"],
#         "confidence": int(session["confidence"] * 100),
#         "ayurveda": ayur,
#         "confidence_explanation": {
#             "symptom_match": session["symptoms"].split(","),
#             "model_reasoning": "LLM + ML agreement",
#             "why_previous_rejected": None
#         },
#         "llm_explanation": (
#             f"{session['disease']} ek condition hai jo aapke symptoms "
#             "aur LLM analysis dono se confirm hui."
#         ),
#         "disclaimer": "Educational & research use only"
#     })

# if __name__ == "__main__":
#     app.run(debug=True)

##################here we are adding the categories #######################

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import uuid, os, json, time
# import joblib
# import pandas as pd
# import requests
# from scipy.sparse import hstack, csr_matrix

# app = Flask(__name__)
# CORS(app)

# # ---------------- PATHS ----------------
# BASE_DIR = os.path.dirname(__file__)
# MODEL_DIR = os.path.join(BASE_DIR, "..", "model")
# DATA_DIR = os.path.join(BASE_DIR, "..", "data")

# MODEL_PATH = os.path.join(MODEL_DIR, "random_forest_large_smote.pkl")
# VECT_PATH = os.path.join(MODEL_DIR, "tfidf_large_smote.pkl")
# AYUR_TEMPLATES = os.path.join(DATA_DIR, "ayurveda_templates.csv")

# # ---------------- LOAD ----------------
# model = joblib.load(MODEL_PATH)
# vectorizer = joblib.load(VECT_PATH)
# ayur_templates_df = pd.read_csv(AYUR_TEMPLATES)

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# # ---------------- LOAD FEATURE CONFIG ----------------
# FEATURE_CONFIG = {"numeric_cols": [], "categorical_cols": []}

# config_path = os.path.join(MODEL_DIR, "feature_config.json")
# if os.path.exists(config_path):
#     with open(config_path) as f:
#         FEATURE_CONFIG = json.load(f)

# scaler, ohe = None, None

# scaler_path = os.path.join(MODEL_DIR, "scaler.pkl")
# ohe_path = os.path.join(MODEL_DIR, "ohe.pkl")

# if os.path.exists(scaler_path):
#     scaler = joblib.load(scaler_path)
# if os.path.exists(ohe_path):
#     ohe = joblib.load(ohe_path)

# SESSIONS = {}
# SESSION_TIMEOUT = 300

# # ---------------- INTAKE QUESTIONS ----------------
# INTAKE_QUESTIONS = [
#     {"id": "age", "question": "What is your age?", "type": "number"},
#     {"id": "gender", "question": "What is your gender?", "type": "choice", "options": ["male","female","other"]},
#     {"id": "duration_days", "question": "How many days have you had symptoms?", "type": "number"},
#     {"id": "fever_pattern", "question": "Fever pattern?", "type": "choice", "options": ["cyclic","sudden","gradual","mild","none"]},
#     {"id": "severity", "question": "Severity?", "type": "choice", "options": ["mild","moderate","severe"]},
#     {"id": "travel_history", "question": "Recent travel?", "type": "choice", "options": ["yes","no"]},
#     {"id": "season", "question": "Current season?", "type": "choice", "options": ["summer","monsoon","winter","spring"]},
#     {"id": "onset_type", "question": "Onset type?", "type": "choice", "options": ["sudden","gradual"]}
# ]

# # ---------------- HELPERS ----------------
# def cleanup_sessions():
#     now = time.time()
#     for sid in list(SESSIONS.keys()):
#         if now - SESSIONS[sid]["created"] > SESSION_TIMEOUT:
#             del SESSIONS[sid]

# def build_feature_vector(symptoms, attributes):
#     X_text = vectorizer.transform([symptoms])
#     parts = [X_text]

#     if scaler and FEATURE_CONFIG["numeric_cols"]:
#         num_vals = []
#         for col in FEATURE_CONFIG["numeric_cols"]:
#             num_vals.append(float(attributes.get(col, 0)))
#         parts.append(csr_matrix(scaler.transform([num_vals])))

#     if ohe and FEATURE_CONFIG["categorical_cols"]:
#         cat_vals = []
#         for col in FEATURE_CONFIG["categorical_cols"]:
#             cat_vals.append(str(attributes.get(col, "unknown")).lower())
#         parts.append(ohe.transform([cat_vals]))

#     return hstack(parts)

# def get_ayurveda(disease, body_type="kapha"):
#     row = ayur_templates_df[
#         ayur_templates_df["disease"].str.lower() == disease.lower()
#     ]
#     if row.empty:
#         return {"herbs":"NA","therapy":"NA","diet":"NA","body_type_effect":"NA"}
#     return {
#         "herbs": row.iloc[0]["herbs"],
#         "therapy": row.iloc[0]["therapy"],
#         "diet": row.iloc[0]["diet"],
#         "body_type_effect": row.iloc[0].get(f"{body_type}_effect","NA")
#     }

# def llm_explain(disease, symptoms, attributes):
#     if not OPENROUTER_API_KEY:
#         return f"Based on your symptoms, {disease} is most likely."

#     prompt = f"""
# Explain in simple Hinglish why this disease is predicted.

# Disease: {disease}
# Symptoms: {symptoms}
# Attributes: {attributes}

# Keep it 2-3 lines.
# """

#     try:
#         res = requests.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             headers={
#                 "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#                 "Content-Type": "application/json"
#             },
#             json={
#                 "model": "openai/gpt-4o-mini",
#                 "messages": [{"role": "user", "content": prompt}],
#                 "temperature": 0.4
#             },
#             timeout=10
#         )
#         return res.json()["choices"][0]["message"]["content"]
#     except:
#         return f"{disease} seems likely based on your inputs."

# def run_prediction(symptoms, attributes):
#     X = build_feature_vector(symptoms, attributes)

#     probs = model.predict_proba(X)[0]
#     ranked = sorted(zip(model.classes_, probs), key=lambda x: x[1], reverse=True)

#     disease, confidence = ranked[0]
#     ayur = get_ayurveda(disease)
#     explanation = llm_explain(disease, symptoms, attributes)

#     return {
#         "status": "final",
#         "predicted_disease": disease,
#         "confidence": int(confidence * 100),
#         "top3": [
#             {"disease": d, "confidence": int(p * 100)}
#             for d, p in ranked[:3]
#         ],
#         "ayurveda": ayur,
#         "ai_explanation": explanation,
#         "disclaimer": "Educational use only"
#     }

# # ---------------- ROUTE ----------------
# @app.route("/predict", methods=["POST"])
# def predict():
#     cleanup_sessions()
#     data = request.json or {}

#     session_id = data.get("session_id")

#     # -------- START --------
#     if "symptoms" in data:
#         session_id = str(uuid.uuid4())
#         SESSIONS[session_id] = {
#             "created": time.time(),
#             "symptoms": data["symptoms"].lower().strip(),
#             "attributes": {},
#             "q_index": 0
#         }

#         q = INTAKE_QUESTIONS[0]

#         return jsonify({
#             "session_id": session_id,
#             "status": "collecting",
#             "question": q["question"],
#             "type": q["type"],
#             "options": q.get("options"),
#             "progress": "1/8"
#         })

#     # -------- ANSWER FLOW --------
#     session = SESSIONS.get(session_id)
#     if not session:
#         return jsonify({"error":"Session expired"}), 400

#     answer = data.get("answer")
#     q_index = session["q_index"]

#     if q_index < len(INTAKE_QUESTIONS):
#         q = INTAKE_QUESTIONS[q_index]
#         session["attributes"][q["id"]] = answer
#         session["q_index"] += 1

#     # more questions
#     if session["q_index"] < len(INTAKE_QUESTIONS):
#         next_q = INTAKE_QUESTIONS[session["q_index"]]
#         return jsonify({
#             "session_id": session_id,
#             "status": "collecting",
#             "question": next_q["question"],
#             "type": next_q["type"],
#             "options": next_q.get("options"),
#             "progress": f"{session['q_index']+1}/8"
#         })

#     # -------- FINAL PREDICTION --------
#     result = run_prediction(session["symptoms"], session["attributes"])
#     del SESSIONS[session_id]
#     return jsonify({
#     "status": "final",
#     "predicted_disease": result["predicted_disease"],
#     "confidence": result["confidence"],
#     "top3": result["top3"],
#     "ayurveda": result["ayurveda"],

#     # text explanation (chat ke liye)
#     "llm_explanation": result["ai_explanation"],

#     # graph ke liye structured explanation
#     "confidence_explanation": {
#         "symptom_match": session["symptoms"].split(),
#         "model_reasoning": result["ai_explanation"],
#         "why_previous_rejected": None
#     },

#     "disclaimer": result["disclaimer"]
# })
# #     return jsonify({
# #     "status": "final",
# #     "predicted_disease": result["predicted_disease"],
# #     "confidence": result["confidence"],  
# #     "top3": result["top3"],               
# #     "ayurveda": result["ayurveda"],
# #     "llm_explanation": result["ai_explanation"],
# #       "confidence_explanation": {
# #         "top3": result["top3"],
# #         "note": "Model probability distribution"
# #     },
# #     "disclaimer": result["disclaimer"]
# # })


# if __name__ == "__main__":
#     app.run(debug=True)



############## added new model datset ######################

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import uuid, os, json, time
# import joblib
# import pandas as pd
# from scipy.sparse import hstack, csr_matrix

# app = Flask(__name__)
# CORS(app)

# # ---------------- PATHS ----------------
# BASE_DIR = os.path.dirname(__file__)
# MODEL_DIR = os.path.join(BASE_DIR, "..", "model")
# DATA_DIR = os.path.join(BASE_DIR, "..", "data")

# MODEL_PATH = os.path.join(MODEL_DIR, "rf_final.pkl")
# VECT_PATH = os.path.join(MODEL_DIR, "tfidf_final.pkl")
# SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
# OHE_PATH = os.path.join(MODEL_DIR, "ohe.pkl")
# CONFIG_PATH = os.path.join(MODEL_DIR, "feature_config.json")

# AYUR_TEMPLATES = os.path.join(DATA_DIR, "ayurveda_templates.csv")

# # ---------------- LOAD ----------------
# model = joblib.load(MODEL_PATH)
# vectorizer = joblib.load(VECT_PATH)
# scaler = joblib.load(SCALER_PATH)
# ohe = joblib.load(OHE_PATH)

# with open(CONFIG_PATH) as f:
#     FEATURE_CONFIG = json.load(f)

# ayur_templates_df = pd.read_csv(AYUR_TEMPLATES)

# SESSIONS = {}
# SESSION_TIMEOUT = 300

# # ---------------- QUESTIONS ----------------
# INTAKE_QUESTIONS = [
#     {"id": "age", "question": "What is your age?", "type": "number"},
#     {"id": "gender", "question": "What is your gender?", "type": "choice", "options": ["male","female","other"]},
#     {"id": "duration_days", "question": "How many days have you had symptoms?", "type": "number"},
#     {"id": "fever_pattern", "question": "Fever pattern?", "type": "choice", "options": ["cyclic","sudden","gradual","mild","none"]},
#     {"id": "severity", "question": "Severity?", "type": "choice", "options": ["mild","moderate","severe"]},
#     {"id": "pain_location", "question": "Where is the pain located?", "type": "choice", "options": ["head","chest","abdomen","joints","scrotal","body","none"]},
#     {"id": "burning_urination", "question": "Burning during urination?", "type": "choice", "options": ["yes","no"]},
#     {"id": "rash", "question": "Do you have rash?", "type": "choice", "options": ["yes","no"]},
#     {"id": "chills", "question": "Do you have chills?", "type": "choice", "options": ["yes","no"]},
#     {"id": "nausea", "question": "Do you have nausea?", "type": "choice", "options": ["yes","no"]},
#     {"id": "onset_type", "question": "Onset type?", "type": "choice", "options": ["sudden","gradual"]}
# ]

# # ---------------- CLEAN SESSION ----------------
# def cleanup_sessions():
#     now = time.time()
#     for sid in list(SESSIONS.keys()):
#         if now - SESSIONS[sid]["created"] > SESSION_TIMEOUT:
#             del SESSIONS[sid]

# # ---------------- FEATURE BUILD ----------------
# def build_feature_vector(symptoms, attributes):

#     #  normalize symptoms
#     symptoms = symptoms.lower().replace("and", ",")
#     # symptoms = symptoms.replace(" ", "_")

#     X_text = vectorizer.transform([symptoms])
#     parts = [X_text]

#     # numeric
#     num_vals = []
#     for col in FEATURE_CONFIG["numeric_cols"]:
#         num_vals.append(float(attributes.get(col, 0)))
#     #parts.append(csr_matrix(scaler.transform([num_vals])))

#     num_df = pd.DataFrame([num_vals], columns=FEATURE_CONFIG["numeric_cols"])
#     parts.append(csr_matrix(scaler.transform(num_df)))


#     # categorical
#     cat_vals = []
#     for col in FEATURE_CONFIG["categorical_cols"]:
#         cat_vals.append(str(attributes.get(col, "unknown")).lower())
#     # parts.append(ohe.transform([cat_vals]))
#     cat_df = pd.DataFrame([cat_vals], columns=FEATURE_CONFIG["categorical_cols"])
#     parts.append(ohe.transform(cat_df))

#     return hstack(parts)

# # ---------------- AYURVEDA ----------------
# def get_ayurveda(disease):
#     row = ayur_templates_df[
#         ayur_templates_df["disease"].str.lower() == disease.lower()
#     ]

#     if row.empty:
#         return {"herbs":"NA","therapy":"NA","diet":"NA"}

#     return {
#         "herbs": row.iloc[0].get("herbs","NA"),
#         "therapy": row.iloc[0].get("therapy","NA"),
#         "diet": row.iloc[0].get("diet","NA")
#     }

# # ---------------- PREDICTION ----------------
# def run_prediction(symptoms, attributes):

#     X = build_feature_vector(symptoms, attributes)

#     probs = model.predict_proba(X)[0]
#     classes = model.classes_

#     ranked = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)

#     disease, confidence = ranked[0]

#     return {
#         "predicted_disease": disease,
#         "confidence": int(confidence * 100),
#         "top3": [
#             {"disease": d, "confidence": int(p * 100)}
#             for d, p in ranked[:3]
#         ]
#     }

# # ---------------- ROUTE ----------------
# @app.route("/predict", methods=["POST"])
# def predict():
#     cleanup_sessions()
#     data = request.json or {}

#     session_id = data.get("session_id")

#     # -------- START --------
#     if "symptoms" in data:
#         session_id = str(uuid.uuid4())
#         SESSIONS[session_id] = {
#             "created": time.time(),
#             "symptoms": data["symptoms"],
#             "attributes": {},
#             "q_index": 0
#         }

#         q = INTAKE_QUESTIONS[0]

#         return jsonify({
#             "session_id": session_id,
#             "status": "collecting",
#             "question": q["question"],
#             "type": q["type"],
#             "options": q.get("options")
#         })

#     # -------- AFTER_RESULT CHAT --------
#     if "message" in data and session_id:
#         session = SESSIONS.get(session_id)
#         if session and session.get("mode") == "chat_after_result":
#             user_msg = data.get("message", "").lower()
#             if "why" in user_msg or "reason" in user_msg:
#                 return jsonify({
#                     "reply": f"The prediction was {session['last_result']['predicted_disease']} based on symptom patterns and clinical features."
#                 })
#             elif "other" in user_msg or "alternative" in user_msg:
#                 return jsonify({
#                     "reply": f"Other possible conditions include: {', '.join([d['disease'] for d in session['last_result']['top3'][1:]])}"
#                 })
#             else:
#                 return jsonify({
#                     "reply": "You can ask about why this prediction was made or possible alternatives."
#                 })

#     # -------- FLOW --------
#     session = SESSIONS.get(session_id)
#     if not session:
#         return jsonify({"error":"Session expired"}), 400

#     answer = data.get("answer")
#     q_index = session["q_index"]

#     if q_index < len(INTAKE_QUESTIONS):
#         q = INTAKE_QUESTIONS[q_index]
#         session["attributes"][q["id"]] = answer
#         session["q_index"] += 1

#     if session["q_index"] < len(INTAKE_QUESTIONS):
#         next_q = INTAKE_QUESTIONS[session["q_index"]]
#         return jsonify({
#             "session_id": session_id,
#             "status": "collecting",
#             "question": next_q["question"],
#             "type": next_q["type"],
#             "options": next_q.get("options")
#         })

#     # -------- FINAL --------
#     # result = run_prediction(session["symptoms"], session["attributes"])
#     # ayur = get_ayurveda(result["predicted_disease"])

#     # # del SESSIONS[session_id]
#     # session["mode"] = "chat_after_result"
#     # session["last_result"] = result

#     # return jsonify({
#     #     "status": "final",
#     #     "predicted_disease": result["predicted_disease"],
#     #     "confidence": result["confidence"],
#     #     "top3": result["top3"],
#     #     "ayurveda": ayur,

#     #     "llm_explanation": "Prediction based on symptoms + medical features",

#     #     "confidence_explanation": {
#     #         "symptom_match": session["symptoms"].split(","),
#     #         "symptom_match": [s.strip() for s in session["symptoms"].split(",")],
#     #         "model_reasoning": "TF-IDF + structured features used",
#     #         "why_previous_rejected": ""
#     #     }
#     # })
#     # ─────────────────────────────────────────────────────────────
# # REPLACE only the final "FINAL" block in your app.py
# # Find this section:   # -------- FINAL --------
# # And replace the entire return jsonify({...}) with this:
# # ─────────────────────────────────────────────────────────────

#     # -------- FINAL --------
#     result = run_prediction(session["symptoms"], session["attributes"])
#     ayur = get_ayurveda(result["predicted_disease"])

#     session["mode"] = "chat_after_result"
#     session["last_result"] = result

#     # ── Build symptom_match list cleanly ──
#     symptom_match = [s.strip().replace("_", " ") for s in session["symptoms"].split(",") if s.strip()]

#     # ── Build model_reasoning string — detailed, human-readable ──
#     attrs = session["attributes"]
#     reasoning_parts = [
#         f"The AI analysed your symptoms using a TF-IDF vectoriser combined with a Random Forest classifier.",
#         f"Your reported symptoms were matched against disease patterns in the training data.",
#     ]
#     clinical = []
#     if attrs.get("chills") == "yes":
#         clinical.append("chills (strong indicator of fever-based infections)")
#     if attrs.get("rash") == "yes":
#         clinical.append("rash (helps narrow to viral or skin conditions)")
#     if attrs.get("burning_urination") == "yes":
#         clinical.append("burning urination (key indicator of urinary tract infection)")
#     fp = attrs.get("fever_pattern", "none")
#     if fp not in ["none", "unknown", ""]:
#         clinical.append(f"a '{fp}' fever pattern")
#     pl = attrs.get("pain_location", "none")
#     if pl not in ["none", "unknown", ""]:
#         clinical.append(f"pain located in the {pl} region")
#     if attrs.get("travel_history") == "yes":
#         clinical.append("recent travel history (raises probability of vector-borne diseases)")

#     if clinical:
#         reasoning_parts.append(
#             f"Key clinical features that influenced this prediction: {', '.join(clinical)}."
#         )
#     reasoning_parts.append(
#         f"These factors together produced the highest probability score for {result['predicted_disease']} "
#         f"at {result['confidence']}% confidence."
#     )

#     model_reasoning = " ".join(reasoning_parts)

#     # ── Why alternatives rejected ──
#     if len(result["top3"]) > 1:
#         alts = [f"{d['disease']} ({d['confidence']}%)" for d in result["top3"][1:]]
#         why_rejected = (
#             f"Other conditions considered were: {', '.join(alts)}. "
#             f"These were ranked lower because your specific symptom combination and clinical features "
#             f"aligned more strongly with {result['predicted_disease']}."
#         )
#     else:
#         why_rejected = ""

#     return jsonify({
#         "status":            "final",
#         "session_id":        session_id,
#         "predicted_disease": result["predicted_disease"],
#         "confidence":        result["confidence"],   # integer e.g. 72  (NOT 0.72)
#         "top3":              result["top3"],
#         "ayurveda":          ayur,

#         "llm_explanation": (
#             f"{result['predicted_disease']} was predicted based on your reported symptoms "
#             f"and clinical features with {result['confidence']}% confidence."
#         ),

#         # ── THIS is what ConfidenceGraph.jsx reads as the `explanation` prop ──
#         "confidence_explanation": {
#             "symptom_match":          symptom_match,    # list of strings
#             "model_reasoning":        model_reasoning,  # detailed paragraph
#             "why_previous_rejected":  why_rejected,     # non-empty string
#         }
#     })

# # ---------------- RUN ----------------
# if __name__ == "__main__":
#     app.run(debug=False)


################################ new feature updated  ################################

from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid, os, json, time
import joblib
import pandas as pd
from scipy.sparse import hstack, csr_matrix

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "..", "model")
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

MODEL_PATH = os.path.join(MODEL_DIR, "rf_final.pkl")
VECT_PATH = os.path.join(MODEL_DIR, "tfidf_final.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
OHE_PATH = os.path.join(MODEL_DIR, "ohe.pkl")
CONFIG_PATH = os.path.join(MODEL_DIR, "feature_config.json")

AYUR_TEMPLATES = os.path.join(DATA_DIR, "ayurveda_templates.csv")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECT_PATH)
scaler = joblib.load(SCALER_PATH)
ohe = joblib.load(OHE_PATH)

with open(CONFIG_PATH) as f:
    FEATURE_CONFIG = json.load(f)

ayur_templates_df = pd.read_csv(AYUR_TEMPLATES)

SESSIONS = {}
SESSION_TIMEOUT = 300

INTAKE_QUESTIONS = [
    {"id": "age", "question": "What is your age?", "type": "number"},
    {"id": "gender", "question": "What is your gender?", "type": "choice", "options": ["male","female","other"]},
    {"id": "duration_days", "question": "How many days have you had symptoms?", "type": "number"},
    {"id": "fever_pattern", "question": "Fever pattern?", "type": "choice", "options": ["cyclic","sudden","gradual","mild","none"]},
    {"id": "severity", "question": "Severity?", "type": "choice", "options": ["mild","moderate","severe"]},
    {"id": "pain_location", "question": "Where is the pain located?", "type": "choice", "options": ["head","chest","abdomen","joints","scrotal","body","none"]},
    {"id": "burning_urination", "question": "Burning during urination?", "type": "choice", "options": ["yes","no"]},
    {"id": "rash", "question": "Do you have rash?", "type": "choice", "options": ["yes","no"]},
    {"id": "chills", "question": "Do you have chills?", "type": "choice", "options": ["yes","no"]},
    {"id": "nausea", "question": "Do you have nausea?", "type": "choice", "options": ["yes","no"]},
    {"id": "onset_type", "question": "Onset type?", "type": "choice", "options": ["sudden","gradual"]}
]

def cleanup_sessions():
    now = time.time()
    for sid in list(SESSIONS.keys()):
        if now - SESSIONS[sid]["created"] > SESSION_TIMEOUT:
            del SESSIONS[sid]

def build_feature_vector(symptoms, attributes):
    symptoms = symptoms.lower().replace("and", ",")
    X_text = vectorizer.transform([symptoms])
    parts = [X_text]

    num_vals = []
    for col in FEATURE_CONFIG["numeric_cols"]:
        num_vals.append(float(attributes.get(col, 0)))
    num_df = pd.DataFrame([num_vals], columns=FEATURE_CONFIG["numeric_cols"])
    parts.append(csr_matrix(scaler.transform(num_df)))

    cat_vals = []
    for col in FEATURE_CONFIG["categorical_cols"]:
        cat_vals.append(str(attributes.get(col, "unknown")).lower())
    cat_df = pd.DataFrame([cat_vals], columns=FEATURE_CONFIG["categorical_cols"])
    parts.append(ohe.transform(cat_df))

    return hstack(parts)

def get_ayurveda(disease):
    row = ayur_templates_df[
        ayur_templates_df["disease"].str.lower() == disease.lower()
    ]
    if row.empty:
        return {"herbs":"NA","therapy":"NA","diet":"NA"}
    return {
        "herbs": row.iloc[0].get("herbs","NA"),
        "therapy": row.iloc[0].get("therapy","NA"),
        "diet": row.iloc[0].get("diet","NA")
    }

def run_prediction(symptoms, attributes):
    X = build_feature_vector(symptoms, attributes)
    probs = model.predict_proba(X)[0]
    classes = model.classes_
    ranked = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)
    disease, confidence = ranked[0]
    return {
        "predicted_disease": disease,
        "confidence": int(confidence * 100),
        "top3": [
            {"disease": d, "confidence": int(p * 100)}
            for d, p in ranked[:3]
        ]
    }

@app.route("/predict", methods=["POST"])
def predict():
    cleanup_sessions()
    data = request.json or {}
    session_id = data.get("session_id")

    if "symptoms" in data:
        session_id = str(uuid.uuid4())
        SESSIONS[session_id] = {
            "created": time.time(),
            "symptoms": data["symptoms"],
            "attributes": {},
            "q_index": 0
        }

        q = INTAKE_QUESTIONS[0]
        return jsonify({
            "session_id": session_id,
            "status": "collecting",
            "question": q["question"],
            "type": q["type"],
            "options": q.get("options")
        })

    if "message" in data and session_id:
        session = SESSIONS.get(session_id)
        if session and session.get("mode") == "chat_after_result":
            user_msg = data.get("message", "").lower()
            if "why" in user_msg or "reason" in user_msg:
                return jsonify({
                    "reply": f"The prediction was {session['last_result']['predicted_disease']} based on symptom patterns and clinical features."
                })
            elif "other" in user_msg or "alternative" in user_msg:
                return jsonify({
                    "reply": f"Other possible conditions include: {', '.join([d['disease'] for d in session['last_result']['top3'][1:]])}"
                })
            else:
                return jsonify({
                    "reply": "You can ask about why this prediction was made or possible alternatives."
                })

    session = SESSIONS.get(session_id)
    if not session:
        return jsonify({"error":"Session expired"}), 400

    answer = data.get("answer")
    q_index = session["q_index"]

    if q_index < len(INTAKE_QUESTIONS):
        q = INTAKE_QUESTIONS[q_index]
        session["attributes"][q["id"]] = answer
        session["q_index"] += 1

    if session["q_index"] < len(INTAKE_QUESTIONS):
        next_q = INTAKE_QUESTIONS[session["q_index"]]
        return jsonify({
            "session_id": session_id,
            "status": "collecting",
            "question": next_q["question"],
            "type": next_q["type"],
            "options": next_q.get("options")
        })

    result = run_prediction(session["symptoms"], session["attributes"])
    ayur = get_ayurveda(result["predicted_disease"])

    session["mode"] = "chat_after_result"
    session["last_result"] = result

    return jsonify({
        "status": "final",
        "session_id": session_id,
        "predicted_disease": result["predicted_disease"],
        "confidence": result["confidence"],
        "top3": result["top3"],
        "ayurveda": ayur,
        "llm_explanation": "Prediction based on symptoms + medical features",
        "confidence_explanation": {
            "symptom_match": [s.strip() for s in session["symptoms"].split(",")],
            "model_reasoning": "TF-IDF + structured features used",
            "why_previous_rejected": "Other conditions had lower probabilities"
        }
    })

if __name__ == "__main__":
    app.run(debug=False)



