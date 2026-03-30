# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer

# # 1. Load dataset
# df = pd.read_csv("data/disease_symptom.csv")

# # 2. Clean text (very simple cleaning)
# df["symptoms"] = df["symptoms"].str.lower().str.strip()

# # 3. Convert text symptoms to numerical features using TF-IDF
# vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(df["symptoms"])

# # 4. Labels (diseases)
# y = df["disease"]

# # 5. Print basic info
# print("Number of samples:", X.shape[0])
# print("Number of symptom features:", X.shape[1])
# print("Diseases:", y.unique())
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Load dataset
df = pd.read_csv("data/disease_symptom.csv")

# 2. Remove rows with missing symptoms
df = df.dropna(subset=["symptoms"])

# 3. Clean text
df["symptoms"] = df["symptoms"].astype(str).str.lower().str.strip()

# 4. Convert symptoms to numerical features using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["symptoms"])

# 5. Labels (diseases)
y = df["disease"]

# 6. Print basic info
print("Number of samples:", X.shape[0])
print("Number of symptom features:", X.shape[1])
print("Diseases:", y.unique())
