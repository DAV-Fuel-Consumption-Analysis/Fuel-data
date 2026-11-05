from pathlib import Path
import pandas as pd
#Data cleaning script-Task #6

# Project folder locations
BASE_DIR = Path(__file__).resolve().parent
input_file = BASE_DIR / "DAV - FUEL.xlsx"
output_file = BASE_DIR / "cleaned_fuel_data.xlsx"

# 1. Load data
df = pd.read_excel(input_file, sheet_name="Sheet1")
print("Original shape:", df.shape)

# 2. Remove empty spacer columns and rename columns
df = df.dropna(axis=1, how="all")
df.columns = ["District", "Year", "Petrol_Price", "Diesel_Price","Petrol_KL", "Diesel_KL", "Total_KL"]

# 3. Remove empty rows and total/summary rows
df = df.dropna(how="all")
df = df[df["District"].notna() & df["Year"].notna()]
df = df[~df["District"].astype(str).str.contains("total|sum", case=False)]

# 4. Clean text and fix data types
df["District"] = df["District"].astype(str).str.strip().str.title()
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
num_cols = ["Petrol_Price", "Diesel_Price", "Petrol_KL", "Diesel_KL", "Total_KL"]
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=["Year"])
df["Year"] = df["Year"].astype(int)

# 5. Remove duplicates
df = df.drop_duplicates(subset=["District", "Year"])

# 6. Handle missing values
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

# 7. Recalculate total and sort
df["Total_KL"] = df["Petrol_KL"] + df["Diesel_KL"]
df = df.sort_values(["District", "Year"]).reset_index(drop=True)

# 8. Rename columns to match DAV_FUEL_CLEANED.xlsx
df = df.rename(columns={
    "Petrol_KL": "Petrol_Consumption",
    "Diesel_KL": "Diesel_Consumption",
    "Total_KL": "Total_Fuel_Consumption",
})

# 9. Show summary
print("\nMissing Values:")
print(df.isnull().sum())
print("\nCleaned Dataset:")
print(df.head(10).to_string(index=False))
print("\nCleaned shape:", df.shape)

# 10. Save cleaned dataset
df.to_excel(output_file, index=False)
print("\nSaved:", output_file)