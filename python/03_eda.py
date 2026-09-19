import pandas as pd
from pathlib import Path

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

# -----------------------------------
# 1. Load cleaned dataset
# -----------------------------------

project_root = Path(__file__).resolve().parent.parent

file_path = (
    project_root
    / "data"
    / "cleaned"
    / "telco_customer_churn_cleaned.csv"
)

df = pd.read_csv(file_path)

print("Dataset shape:", df.shape)


# -----------------------------------
# 2. Overall churn
# -----------------------------------

print("\n========== OVERALL CHURN ==========")

churn_counts = df["Churn"].value_counts()

print(churn_counts)

churn_rate = df["ChurnFlag"].mean() * 100

print(f"\nOverall churn rate: {churn_rate:.2f}%")


# -----------------------------------
# 3. Customer demographics
# -----------------------------------

print("\n========== GENDER ==========")
print(pd.crosstab(
    df["gender"],
    df["Churn"],
    normalize="index"
).mul(100).round(2))


print("\n========== SENIOR CITIZEN ==========")
print(pd.crosstab(
    df["SeniorCitizen"],
    df["Churn"],
    normalize="index"
).mul(100).round(2))


print("\n========== PARTNER ==========")
print(pd.crosstab(
    df["Partner"],
    df["Churn"],
    normalize="index"
).mul(100).round(2))


print("\n========== DEPENDENTS ==========")
print(pd.crosstab(
    df["Dependents"],
    df["Churn"],
    normalize="index"
).mul(100).round(2))


# -----------------------------------
# 4. Contract analysis
# -----------------------------------

print("\n========== CONTRACT ==========")

contract_analysis = (
    df.groupby("Contract")
    .agg(
        Customers=("customerID", "count"),
        Churned=("ChurnFlag", "sum"),
        ChurnRate=("ChurnFlag", "mean")
    )
    .sort_values("ChurnRate", ascending=False)
)

contract_analysis["ChurnRate"] = (
    contract_analysis["ChurnRate"] * 100
).round(2)

print(contract_analysis)


# -----------------------------------
# 5. Internet service analysis
# -----------------------------------

print("\n========== INTERNET SERVICE ==========")

internet_analysis = (
    df.groupby("InternetService")
    .agg(
        Customers=("customerID", "count"),
        Churned=("ChurnFlag", "sum"),
        ChurnRate=("ChurnFlag", "mean")
    )
)

internet_analysis["ChurnRate"] = (
    internet_analysis["ChurnRate"] * 100
).round(2)

print(internet_analysis)


# -----------------------------------
# 6. Payment method analysis
# -----------------------------------

print("\n========== PAYMENT METHOD ==========")

payment_analysis = (
    df.groupby("PaymentMethod")
    .agg(
        Customers=("customerID", "count"),
        Churned=("ChurnFlag", "sum"),
        ChurnRate=("ChurnFlag", "mean")
    )
    .sort_values("ChurnRate", ascending=False)
)

payment_analysis["ChurnRate"] = (
    payment_analysis["ChurnRate"] * 100
).round(2)

print(payment_analysis)


# -----------------------------------
# 7. Tenure analysis
# -----------------------------------

print("\n========== TENURE ==========")

print(
    df.groupby("Churn")["tenure"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(2)
)


# -----------------------------------
# 8. Monthly charges analysis
# -----------------------------------

print("\n========== MONTHLY CHARGES ==========")

print(
    df.groupby("Churn")["MonthlyCharges"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(2)
)


# -----------------------------------
# 9. Total charges analysis
# -----------------------------------

print("\n========== TOTAL CHARGES ==========")

print(
    df.groupby("Churn")["TotalCharges"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(2)
)


# -----------------------------------
# 10. Support services
# -----------------------------------

support_columns = [
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport"
]

print("\n========== SUPPORT SERVICES ==========")

for column in support_columns:

    analysis = (
        df.groupby(column)["ChurnFlag"]
        .mean()
        .mul(100)
        .round(2)
    )

    print(f"\n{column}:")
    print(analysis)

# -----------------------------------
# 11. Tenure groups
# -----------------------------------

print("\n========== TENURE GROUPS ==========")

df["TenureGroup"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 48, 72],
    labels=[
        "0-12 months",
        "13-24 months",
        "25-48 months",
        "49-72 months"
    ]
)

tenure_analysis = (
    df.groupby("TenureGroup", observed=True)
    .agg(
        Customers=("customerID", "count"),
        Churned=("ChurnFlag", "sum"),
        ChurnRate=("ChurnFlag", "mean")
    )
)

tenure_analysis["ChurnRate"] = (
    tenure_analysis["ChurnRate"] * 100
).round(2)

print(tenure_analysis)


# -----------------------------------
# 12. Tenure Group × Contract
# -----------------------------------

print("\n========== TENURE GROUP × CONTRACT ==========")

tenure_contract = pd.crosstab(
    df["TenureGroup"],
    df["Contract"],
    values=df["ChurnFlag"],
    aggfunc="mean"
) * 100

print(tenure_contract.round(2))


# -----------------------------------
# 13. Contract × Internet Service
# -----------------------------------

print("\n========== CONTRACT × INTERNET SERVICE ==========")

contract_internet = pd.crosstab(
    df["Contract"],
    df["InternetService"],
    values=df["ChurnFlag"],
    aggfunc="mean"
) * 100

print(contract_internet.round(2))


# -----------------------------------
# 14. Contract × Payment Method
# -----------------------------------

print("\n========== CONTRACT × PAYMENT METHOD ==========")

contract_payment = pd.crosstab(
    df["Contract"],
    df["PaymentMethod"],
    values=df["ChurnFlag"],
    aggfunc="mean"
) * 100

print(contract_payment.round(2))