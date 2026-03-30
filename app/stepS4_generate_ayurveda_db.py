# import pandas as pd

# # Load disease categories
# disease_df = pd.read_csv("data/disease_categories.csv")

# # Load Ayurveda templates
# template_df = pd.read_csv("data/ayurveda_templates.csv")

# # Merge disease with templates
# ayurveda_db = disease_df.merge(template_df, on="category", how="left")

# # Save final Ayurveda database
# ayurveda_db.to_csv("data/ayurveda_large.csv", index=False)

# print("Ayurveda database generated successfully")
# print("Total diseases covered:", ayurveda_db.shape[0])
#############one mistake of category column fixed ####################
import pandas as pd

# Load disease categories
disease_df = pd.read_csv("data/disease_categories.csv")

# Load Ayurveda templates
template_df = pd.read_csv("data/ayurveda_templates.csv")

# 🔍 Debug print (very important)
print("Disease categories columns:", disease_df.columns.tolist())
print("Ayurveda template columns:", template_df.columns.tolist())

# Strip spaces from column names (SAFETY)
disease_df.columns = disease_df.columns.str.strip().str.lower()
template_df.columns = template_df.columns.str.strip().str.lower()

# Merge disease with templates
ayurveda_db = disease_df.merge(template_df, on="category", how="left")

# Save final Ayurveda database
ayurveda_db.to_csv("data/ayurveda_large.csv", index=False)

print("Ayurveda database generated successfully")
print("Total diseases covered:", ayurveda_db.shape[0])

################no useeeeeeeeeeeeeeeeeeeeeeee for now#######################