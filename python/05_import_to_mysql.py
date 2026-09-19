from dotenv import load_dotenv
import os
import pandas as pd
import mysql.connector
from pathlib import Path

# Project paths
project_root = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(project_root / ".env")

csv_file = (
    project_root
    / "data"
    / "cleaned"
    / "telco_customer_churn_cleaned.csv"
)

# Read cleaned CSV
df = pd.read_csv(csv_file)

print("Rows in CSV:", len(df))
print("Columns:", len(df.columns))

# Connect to MySQL
conn = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

cursor = conn.cursor()

# Insert query
query = """
INSERT INTO customers (
    customerID,
    gender,
    SeniorCitizen,
    Partner,
    Dependents,
    tenure,
    PhoneService,
    MultipleLines,
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport,
    StreamingTV,
    StreamingMovies,
    Contract,
    PaperlessBilling,
    PaymentMethod,
    MonthlyCharges,
    TotalCharges,
    Churn,
    ChurnFlag
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""

# Convert NaN to None for MySQL
df = df.where(pd.notnull(df), None)

# Insert rows
data = [tuple(row) for row in df.itertuples(index=False, name=None)]

cursor.executemany(query, data)

conn.commit()

print("Rows inserted:", cursor.rowcount)

cursor.close()
conn.close()

print("MySQL import completed successfully.")