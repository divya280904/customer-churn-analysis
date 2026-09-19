import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------------
# 1. Paths
# -----------------------------------

project_root = Path(__file__).resolve().parent.parent

input_file = (
    project_root
    / "data"
    / "cleaned"
    / "telco_customer_churn_cleaned.csv"
)

image_dir = project_root / "images"

image_dir.mkdir(exist_ok=True)

df = pd.read_csv(input_file)


# -----------------------------------
# 2. Overall Churn
# -----------------------------------

churn_counts = df["Churn"].value_counts()

plt.figure(figsize=(8, 5))

churn_counts.plot(kind="bar")

plt.title("Customer Churn Distribution")
plt.xlabel("Churn")
plt.ylabel("Number of Customers")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    image_dir / "01_churn_distribution.png",
    dpi=300
)

plt.show()


# -----------------------------------
# 3. Churn by Contract
# -----------------------------------

contract_churn = (
    df.groupby("Contract")["ChurnFlag"]
    .mean()
    .mul(100)
)

plt.figure(figsize=(8, 5))

contract_churn.plot(kind="bar")

plt.title("Churn Rate by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Churn Rate (%)")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    image_dir / "02_churn_by_contract.png",
    dpi=300
)

plt.show()


# -----------------------------------
# 4. Churn by Tenure Group
# -----------------------------------

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

tenure_churn = (
    df.groupby("TenureGroup", observed=True)["ChurnFlag"]
    .mean()
    .mul(100)
)

plt.figure(figsize=(8, 5))

tenure_churn.plot(kind="bar")

plt.title("Churn Rate by Customer Tenure")
plt.xlabel("Tenure Group")
plt.ylabel("Churn Rate (%)")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    image_dir / "03_churn_by_tenure.png",
    dpi=300
)

plt.show()


# -----------------------------------
# 5. Churn by Payment Method
# -----------------------------------

payment_churn = (
    df.groupby("PaymentMethod")["ChurnFlag"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))

payment_churn.plot(kind="bar")

plt.title("Churn Rate by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Churn Rate (%)")

plt.xticks(rotation=30, ha="right")

plt.tight_layout()

plt.savefig(
    image_dir / "04_churn_by_payment_method.png",
    dpi=300
)

plt.show()


print("\nVisualizations saved successfully to:")
print(image_dir)

# Churn Rate: Tenure Group vs Contract
tenure_contract = (
    df.groupby(["TenureGroup", "Contract"], observed=True)["ChurnFlag"]
    .mean()
    .mul(100)
    .unstack()
)

plt.figure(figsize=(10, 6))
tenure_contract.plot(kind="bar")
plt.title("Churn Rate by Tenure Group and Contract Type")
plt.xlabel("Tenure Group")
plt.ylabel("Churn Rate (%)")
plt.xticks(rotation=0)
plt.legend(title="Contract Type")
plt.tight_layout()
plt.savefig(image_dir / "05_churn_tenure_contract.png", dpi=300)
plt.show()


# Churn Rate: Contract vs Internet Service
contract_internet = (
    df.groupby(["Contract", "InternetService"])["ChurnFlag"]
    .mean()
    .mul(100)
    .unstack()
)

plt.figure(figsize=(10, 6))
contract_internet.plot(kind="bar")
plt.title("Churn Rate by Contract and Internet Service")
plt.xlabel("Contract Type")
plt.ylabel("Churn Rate (%)")
plt.xticks(rotation=0)
plt.legend(title="Internet Service")
plt.tight_layout()
plt.savefig(image_dir / "06_churn_contract_internet.png", dpi=300)
plt.show()


# Monthly Charges: Churned vs Retained
plt.figure(figsize=(8, 5))
df.boxplot(column="MonthlyCharges", by="Churn")
plt.title("Monthly Charges by Churn Status")
plt.suptitle("")
plt.xlabel("Churn")
plt.ylabel("Monthly Charges")
plt.tight_layout()
plt.savefig(image_dir / "07_monthly_charges_by_churn.png", dpi=300)
plt.show()


print("\nAll visualizations saved successfully.")