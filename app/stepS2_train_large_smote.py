# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from imblearn.over_sampling import SMOTE
# import joblib

# # Load large dataset
# df = pd.read_csv("data/disease_symptom_large.csv")

# # Clean data
# df = df.dropna(subset=["symptoms"])
# df["symptoms"] = df["symptoms"].astype(str).str.lower().str.strip()

# # TF-IDF vectorization
# vectorizer = TfidfVectorizer(max_features=1000)
# X = vectorizer.fit_transform(df["symptoms"])
# y = df["disease"]

# print("Original dataset size:", X.shape, y.nunique(), "diseases")

# # Train-test split
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42, stratify=y
# )

# # Apply SMOTE (IMPORTANT STEP)
# smote = SMOTE(random_state=42)
# X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# print("After SMOTE:", X_train_smote.shape, len(set(y_train_smote)), "diseases")

# # Train Random Forest
# model = RandomForestClassifier(
#     n_estimators=300,
#     random_state=42,
#     n_jobs=-1
# )
# model.fit(X_train_smote, y_train_smote)

# # Evaluate
# y_pred = model.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)

# print("SMOTE Model Training Completed")
# print("Accuracy:", accuracy)

# # Save model
# joblib.dump(model, "model/random_forest_large_smote.pkl")
# joblib.dump(vectorizer, "model/tfidf_large_smote.pkl")

# print("SMOTE-based large model saved successfully")

#######################################################################################

#somte overcome SMOTE bhi minimum 2 samples mangta hai per class 
#Stratify temporarily remove karo
#Pehle SMOTE-ready dataset banao
#Fir future me jab data bade, stratify add karenge


# So hum ek SMART workaround use karenge

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
import joblib

# Load large dataset
df = pd.read_csv("data/disease_symptom_large.csv")

# Clean data
df = df.dropna(subset=["symptoms"])
df["symptoms"] = df["symptoms"].astype(str).str.lower().str.strip()

# TF-IDF
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df["symptoms"])
y = df["disease"]

print("Total samples:", X.shape[0])
print("Total diseases:", y.nunique())

# ⚠️ IMPORTANT: NO STRATIFY HERE (because many classes have only 1 sample)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Apply SMOTE safely
smote = SMOTE(random_state=42, k_neighbors=1)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print("After SMOTE samples:", X_train_smote.shape[0])
print("Diseases after SMOTE:", len(set(y_train_smote)))

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train_smote, y_train_smote)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("SMOTE Model Training Completed")
print("Accuracy:", accuracy)

# Save model
joblib.dump(model, "model/random_forest_large_smote.pkl")
joblib.dump(vectorizer, "model/tfidf_large_smote.pkl")

print("SMOTE-based large model saved successfully")
#######################################################################################