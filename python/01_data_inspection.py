import pandas as pd
from pathlib import Path

# -----------------------------
# 1. Load dataset
# -----------------------------

project_root = Path(__file__).resolve().parent.parent

file_path = project_root / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"

df = pd.read_csv(file_path)

# -----------------------------
# 2. Basic information
# -----------------------------

print("\n========== DATASET SHAPE ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

# -----------------------------
# 3. First 5 rows
# -----------------------------

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

# -----------------------------
# 4. Data types
# -----------------------------

print("\n========== DATA TYPES ==========")
print(df.dtypes)

# -----------------------------
# 5. Missing values
# -----------------------------

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# -----------------------------
# 6. Duplicate rows
# -----------------------------

print("\n========== DUPLICATES ==========")
print("Duplicate rows:", df.duplicated().sum())

# -----------------------------
# 7. Unique values
# -----------------------------

print("\n========== UNIQUE VALUES ==========")

for column in df.columns:
    print(f"\n{column}:")
    print(df[column].unique()[:20])

# -----------------------------
# 8. Statistical summary
# -----------------------------

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe(include="all"))