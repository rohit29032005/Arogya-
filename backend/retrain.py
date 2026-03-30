# import pandas as pd
# import numpy as np
# import joblib
# import os
# import json
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.preprocessing import StandardScaler, OneHotEncoder
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report
# from imblearn.over_sampling import SMOTE
# from scipy.sparse import hstack

# # ========================= PATHS =========================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_DIR = os.path.join(BASE_DIR, "..", "data")
# DATA_PATH = os.path.join(DATA_DIR, "ready_for_model_training.csv")

# MODEL_DIR = "model"
# os.makedirs(MODEL_DIR, exist_ok=True)

# # ========================= LOAD DATA =========================
# print("Loading dataset...")
# df = pd.read_csv(DATA_PATH)

# # Basic cleaning
# df['symptoms'] = df['symptoms'].astype(str).str.lower().str.strip()
# df = df.dropna(subset=['symptoms', 'disease'])

# print(f"Dataset shape: {df.shape}")
# print(f"Unique diseases: {df['disease'].nunique()}")

# # ========================= DEFINE COLUMNS =========================
# TEXT_COL = 'symptoms'
# TARGET = 'disease'

# NUMERIC_COLS = ['age', 'duration_days']
# CATEGORICAL_COLS = ['gender', 'fever_pattern', 'severity', 'travel_history', 'season', 'onset_type']

# # Fill missing values safely
# for col in NUMERIC_COLS:
#     df[col] = pd.to_numeric(df[col], errors='coerce')
#     df[col] = df[col].fillna(df[col].median())

# for col in CATEGORICAL_COLS:
#     df[col] = df[col].astype(str).fillna('unknown')

# # ========================= FEATURE ENGINEERING =========================
# print("Building features...")

# # 1. Text Features (TF-IDF)
# tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=12000, min_df=2, sublinear_tf=True)
# X_text = tfidf.fit_transform(df[TEXT_COL])

# # 2. Numeric Features
# scaler = StandardScaler()
# X_num = scaler.fit_transform(df[NUMERIC_COLS])

# # 3. Categorical Features
# ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
# X_cat = ohe.fit_transform(df[CATEGORICAL_COLS])

# # 4. Combine all (hstack)
# X = hstack([X_text, X_num, X_cat])
# y = df[TARGET].values

# print(f"Final feature matrix shape: {X.shape}")

# # ========================= TRAIN-TEST SPLIT + SMOTE =========================
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# smote = SMOTE(random_state=42, k_neighbors=5)
# X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# print(f"After SMOTE - Train samples: {X_train_res.shape[0]}")

# # ========================= MODEL TRAINING =========================
# print("Training Random Forest...")
# model = RandomForestClassifier(
#     n_estimators=300,
#     max_depth=None,
#     min_samples_split=2,
#     class_weight="balanced",
#     random_state=42,
#     n_jobs=-1
# )

# model.fit(X_train_res, y_train_res)

# # ========================= EVALUATION =========================
# y_pred = model.predict(X_test)
# print("\nClassification Report:")
# print(classification_report(y_test, y_pred, digits=4))

# # ========================= SAVE EVERYTHING =========================
# joblib.dump(model, os.path.join(MODEL_DIR, "random_forest_large_smote.pkl"))
# joblib.dump(tfidf, os.path.join(MODEL_DIR, "tfidf_large_smote.pkl"))
# joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
# joblib.dump(ohe, os.path.join(MODEL_DIR, "ohe.pkl"))

# # Save feature config for app.py
# feature_config = {
#     "numeric_cols": NUMERIC_COLS,
#     "categorical_cols": CATEGORICAL_COLS,
#     "text_max_features": 12000
# }
# with open(os.path.join(MODEL_DIR, "feature_config.json"), "w") as f:
#     json.dump(feature_config, f, indent=2)

# print(f"\n✅ All models saved in '{MODEL_DIR}/' folder!")
# print("Files saved:")
# print("   • random_forest_large_smote.pkl")
# print("   • tfidf_large_smote.pkl")
# print("   • scaler.pkl")
# print("   • ohe.pkl")
# print("   • feature_config.json")

# import pandas as pd
# import numpy as np
# import joblib
# import os
# import json
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.preprocessing import StandardScaler, OneHotEncoder
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from imblearn.over_sampling import SMOTE
# from scipy.sparse import hstack

# # ========================= PATHS =========================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_DIR = os.path.join(BASE_DIR, "..", "data")
# DATA_PATH = os.path.join(DATA_DIR, "ready_for_model_training.csv")

# MODEL_DIR = os.path.join(BASE_DIR, "model")
# os.makedirs(MODEL_DIR, exist_ok=True)

# # ========================= LOAD DATA =========================
# df = pd.read_csv(DATA_PATH)
# df['symptoms'] = df['symptoms'].astype(str).str.lower().str.strip()

# print(f"Original rows: {len(df)} | Unique diseases: {df['disease'].nunique()}")

# # === FIX: Remove diseases with very few samples ===
# min_samples = 2
# disease_counts = df['disease'].value_counts()
# rare_diseases = disease_counts[disease_counts < min_samples].index
# df = df[~df['disease'].isin(rare_diseases)]

# print(f"After removing rare classes (< {min_samples} samples): {len(df)} rows | Unique diseases: {df['disease'].nunique()}")

# # ========================= COLUMNS =========================
# NUMERIC_COLS = ['age', 'duration_days']
# CATEGORICAL_COLS = ['gender', 'fever_pattern', 'severity', 'travel_history', 'season', 'onset_type']

# for col in NUMERIC_COLS:
#     df[col] = pd.to_numeric(df[col], errors='coerce')
#     df[col] = df[col].fillna(df[col].median())

# for col in CATEGORICAL_COLS:
#     df[col] = df[col].astype(str).fillna('unknown')

# # ========================= FEATURES =========================
# tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=12000, min_df=2, sublinear_tf=True)
# X_text = tfidf.fit_transform(df['symptoms'])

# scaler = StandardScaler()
# X_num = scaler.fit_transform(df[NUMERIC_COLS])

# ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
# X_cat = ohe.fit_transform(df[CATEGORICAL_COLS])

# X = hstack([X_text, X_num, X_cat])
# y = df['disease'].values

# print(f"Final feature shape: {X.shape}")

# # ========================= TRAIN-TEST SPLIT =========================
# # stratify=y ab safe hai kyunki har class mein kam se kam 2 samples hain
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42, stratify=y
# )

# smote = SMOTE(random_state=42 , k_neighbors=2)
# X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# # ========================= MODEL =========================
# model = RandomForestClassifier(
#     n_estimators=300,
#     random_state=42,
#     n_jobs=-1,
#     class_weight="balanced"
# )
# model.fit(X_train_res, y_train_res)

# # ========================= SAVE =========================
# joblib.dump(model, os.path.join(MODEL_DIR, "random_forest_large_smote.pkl"))
# joblib.dump(tfidf, os.path.join(MODEL_DIR, "tfidf_large_smote.pkl"))
# joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
# joblib.dump(ohe, os.path.join(MODEL_DIR, "ohe.pkl"))

# feature_config = {
#     "numeric_cols": NUMERIC_COLS,
#     "categorical_cols": CATEGORICAL_COLS
# }
# with open(os.path.join(MODEL_DIR, "feature_config.json"), "w") as f:
#     json.dump(feature_config, f, indent=2)

# print("\n🎉 Training Completed Successfully!")
# print(f"Final unique diseases after cleaning: {df['disease'].nunique()}")

################### new dataset has been loaded ############################

import pandas as pd
import numpy as np
import joblib
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from scipy.sparse import hstack

# ================= PATHS =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DATA_PATH = os.path.join(DATA_DIR, "ready_for_model_training_v3.csv")
MODEL_DIR = os.path.join(BASE_DIR, "..", "model")
os.makedirs(MODEL_DIR, exist_ok=True)

# ================= LOAD =================
df = pd.read_csv(DATA_PATH)
df['symptoms'] = df['symptoms'].astype(str).str.lower().str.strip()

# ================= FILTER =================
min_samples = 2
counts = df['disease'].value_counts()
df = df[df['disease'].isin(counts[counts >= min_samples].index)]

# ================= COLUMNS =================
NUMERIC_COLS = ['age', 'duration_days']

CATEGORICAL_COLS = [
 'gender','fever_pattern','severity',
 'travel_history','season','onset_type',
 'pain_location','burning_urination',
 'rash','chills','nausea'
]

# ================= CLEAN =================
for col in NUMERIC_COLS:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(df[col].median())

for col in CATEGORICAL_COLS:
    df[col] = df[col].astype(str).fillna('unknown')

# ================= FEATURES =================
tfidf = TfidfVectorizer(ngram_range=(1,2), max_features=10000)
X_text = tfidf.fit_transform(df['symptoms'])

scaler = StandardScaler()
X_num = scaler.fit_transform(df[NUMERIC_COLS])

ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
X_cat = ohe.fit_transform(df[CATEGORICAL_COLS])

X = hstack([X_text, X_num, X_cat])
y = df['disease']

# ================= SPLIT =================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ================= SMOTE =================
smote = SMOTE(random_state=42, k_neighbors=2)
X_train, y_train = smote.fit_resample(X_train, y_train)

# ================= MODEL =================
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# ================= SAVE =================
joblib.dump(model, os.path.join(MODEL_DIR, "rf_final.pkl"))
joblib.dump(tfidf, os.path.join(MODEL_DIR, "tfidf_final.pkl"))
joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
joblib.dump(ohe, os.path.join(MODEL_DIR, "ohe.pkl"))

config = {
    "numeric_cols": NUMERIC_COLS,
    "categorical_cols": CATEGORICAL_COLS
}

with open(os.path.join(MODEL_DIR, "feature_config.json"), "w") as f:
    json.dump(config, f)

print("🔥 MODEL READY")
print("Saving to:", MODEL_DIR)