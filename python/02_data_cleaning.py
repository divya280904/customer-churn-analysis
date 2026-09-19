import pandas as pd
from pathlib import Path

# -----------------------------------
# 1. Define paths
# -----------------------------------

project_root = Path(__file__).resolve().parent.parent

input_file = (
    project_root
    / "data"
    / "raw"
    / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

output_file = (
    project_root
    / "data"
    / "cleaned"
    / "telco_customer_churn_cleaned.csv"
)

# -----------------------------------
# 2. Load raw dataset
# -----------------------------------

df = pd.read_csv(input_file)

print("Original shape:", df.shape)

# -----------------------------------
# 3. Check blank TotalCharges values
# -----------------------------------

blank_total_charges = (df["TotalCharges"].str.strip() == "").sum()

print("Blank TotalCharges values:", blank_total_charges)

# -----------------------------------
# 4. Convert blank strings to NaN
# -----------------------------------

df["TotalCharges"] = df["TotalCharges"].replace(r"^\s*$", pd.NA, regex=True)

# -----------------------------------
# 5. Convert TotalCharges to numeric
# -----------------------------------

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

# -----------------------------------
# 6. Check missing values again
# -----------------------------------

print("\nMissing values after conversion:")
print(df.isnull().sum())

# -----------------------------------
# 7. Handle missing TotalCharges
# -----------------------------------

missing_total_charges = df["TotalCharges"].isnull().sum()

print("\nMissing TotalCharges:", missing_total_charges)

# These customers have zero tenure,
# so their total charges should be 0.
df.loc[
    df["TotalCharges"].isnull() & (df["tenure"] == 0),
    "TotalCharges"
] = 0

# -----------------------------------
# 8. Convert SeniorCitizen to category
# -----------------------------------

df["SeniorCitizen"] = df["SeniorCitizen"].map({
    0: "No",
    1: "Yes"
})

# -----------------------------------
# 9. Create useful numeric churn flag
# -----------------------------------

df["ChurnFlag"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

# -----------------------------------
# 10. Remove duplicate rows
# -----------------------------------

before_duplicates = len(df)

df = df.drop_duplicates()

after_duplicates = len(df)

print(
    "\nDuplicates removed:",
    before_duplicates - after_duplicates
)

# -----------------------------------
# 11. Final validation
# -----------------------------------

print("\n========== FINAL DATASET ==========")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nFirst 5 rows:")
print(df.head())

# -----------------------------------
# 12. Save cleaned dataset
# -----------------------------------

df.to_csv(output_file, index=False)

print("\nCleaned dataset saved to:")
print(output_file)