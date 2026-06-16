import pandas as pd
from pathlib import Path

input_path = Path("data/lightcast_job_postings.csv")
output_path = Path("data/lightcast_job_postings_cleaned.csv")

df = pd.read_csv(input_path, low_memory=False)

# 1. Remove duplicate rows
df = df.drop_duplicates()

# 2. Standardize column names
df.columns = [c.strip() for c in df.columns]

# 3. Convert salary and experience columns to numeric
numeric_cols = [
    "SALARY",
    "SALARY_FROM",
    "SALARY_TO",
    "MIN_YEARS_EXPERIENCE",
    "MAX_YEARS_EXPERIENCE",
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# 4. Create Average_Salary
if "SALARY_FROM" in df.columns and "SALARY_TO" in df.columns:
    df["Average_Salary"] = df[["SALARY_FROM", "SALARY_TO"]].mean(axis=1)

if "SALARY" in df.columns:
    df["Average_Salary"] = df["Average_Salary"].fillna(df["SALARY"])

# 5. Fill missing salary with median
median_salary = df["Average_Salary"].median()
df["Average_Salary"] = df["Average_Salary"].fillna(median_salary)

if "SALARY" in df.columns:
    df["SALARY"] = df["SALARY"].fillna(median_salary)

# 6. Clean education column
if "EDUCATION_LEVELS_NAME" in df.columns:
    df["EDUCATION_LEVELS_NAME"] = (
        df["EDUCATION_LEVELS_NAME"]
        .astype(str)
        .str.replace(r"[\n\r]", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

# 7. Clean remote type
if "REMOTE_TYPE_NAME" in df.columns:
    df["REMOTE_GROUP"] = df["REMOTE_TYPE_NAME"].fillna("Onsite")
    df["REMOTE_GROUP"] = df["REMOTE_GROUP"].replace(["[None]", "", "nan"], "Onsite")

# 8. Keep cleaned file
df.to_csv(output_path, index=False)

print("Cleaned data exported successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {output_path}")