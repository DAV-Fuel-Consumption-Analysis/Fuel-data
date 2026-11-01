import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- LOAD DATA ----------
BASE = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE, "DAV - FUEL.xlsx")   # your exact file name

df = pd.read_excel(FILE, sheet_name="Sheet1")
df = df.dropna(axis=1, how="all")
df.columns = ["District", "Year", "Petrol_Price", "Diesel_Price",
              "Petrol_KL", "Diesel_KL", "Total_KL"]
df = df.dropna(subset=["District", "Year"])
df["Year"] = df["Year"].astype(int)
sns.set_style("whitegrid")

def save(name):
    plt.tight_layout()
    plt.savefig(os.path.join(BASE, name), dpi=150)
    plt.close()

# ---------- 1. MEAN, MEDIAN, MODE, STD ----------
cols = ["Petrol_KL", "Diesel_KL", "Total_KL", "Petrol_Price", "Diesel_Price"]
stats = pd.DataFrame({
    "Mean": df[cols].mean(),
    "Median": df[cols].median(),
    "Mode": df[cols].mode().iloc[0],
    "Std Dev": df[cols].std(),
}).round(2)
print("\n===== MEAN, MEDIAN, MODE, STD DEV =====")
print(stats.to_string())

# ---------- 2. HISTOGRAM ----------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.histplot(df["Petrol_KL"], bins=15, kde=True, color="#1d3557", ax=axes[0])
axes[0].set_title("Petrol Consumption Distribution")
sns.histplot(df["Diesel_KL"], bins=15, kde=True, color="#e63946", ax=axes[1])
axes[1].set_title("Diesel Consumption Distribution")
save("Histogram.png")

# ---------- 3. BOX PLOT ----------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.boxplot(data=df, x="Year", y="Petrol_KL", color="#457b9d", ax=axes[0])
axes[0].set_title("Petrol Consumption by Year")
sns.boxplot(data=df, x="Year", y="Diesel_KL", color="#e76f51", ax=axes[1])
axes[1].set_title("Diesel Consumption by Year")
save("BoxPlot.png")

# ---------- 4. PETROL VS DIESEL SCATTER ----------
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="Petrol_KL", y="Diesel_KL", hue="Year",
                palette="viridis", s=70)
m, c = np.polyfit(df["Petrol_KL"], df["Diesel_KL"], 1)
xs = np.linspace(df["Petrol_KL"].min(), df["Petrol_KL"].max(), 100)
plt.plot(xs, m * xs + c, color="black", linestyle="--", label="Trend line")
plt.title("Petrol vs Diesel Consumption (per district-year)")
plt.xlabel("Petrol (KL)"); plt.ylabel("Diesel (KL)"); plt.legend()
save("Scatter_Petrol_vs_Diesel.png")

# ---------- 5. YEAR-OVER-YEAR GROWTH ----------
yearly = df.groupby("Year")[["Petrol_KL", "Diesel_KL", "Total_KL"]].sum()
yoy = (yearly.pct_change() * 100).round(2).dropna()
print("\n===== YEAR-OVER-YEAR GROWTH (%) =====")
print(yoy.to_string())
yoy.plot(kind="bar", figsize=(9, 5), color=["#1d3557", "#e63946", "#2a9d8f"])
plt.title("Year-over-Year Growth (%)"); plt.ylabel("Growth %"); plt.xticks(rotation=0)
save("YoY_Growth.png")

# ---------- 6. DISTRICT RANKING ----------
ranking = (df.groupby("District")[["Petrol_KL", "Diesel_KL", "Total_KL"]].sum()
           .sort_values("Total_KL", ascending=False).reset_index())
ranking.insert(0, "Rank", range(1, len(ranking) + 1))
ranking["Share_%"] = (ranking["Total_KL"] / ranking["Total_KL"].sum() * 100).round(2)
print("\n===== DISTRICT RANKING =====")
print(ranking.to_string(index=False))
top10 = ranking.head(10).iloc[::-1]
plt.figure(figsize=(10, 6))
plt.barh(top10["District"], top10["Total_KL"], color="#2a6f97")
plt.title("Top 10 Districts by Total Fuel Consumption"); plt.xlabel("KL")
save("District_Ranking.png")

# ---------- 7. KPI SUMMARY ----------
total = df["Total_KL"].sum()
kpi = {
    "Total Consumption (KL)": f"{total:,.0f}",
    "Petrol Share (%)": f"{df['Petrol_KL'].sum() / total * 100:.2f}",
    "Diesel Share (%)": f"{df['Diesel_KL'].sum() / total * 100:.2f}",
    "Top District": ranking.iloc[0]["District"],
    "Lowest District": ranking.iloc[-1]["District"],
    "Avg Petrol Price (INR/L)": f"{df['Petrol_Price'].mean():.2f}",
    "Avg Diesel Price (INR/L)": f"{df['Diesel_Price'].mean():.2f}",
    "Overall Growth 2023-2026 (%)":
        f"{(yearly['Total_KL'].iloc[-1] / yearly['Total_KL'].iloc[0] - 1) * 100:.2f}",
}
print("\n===== KPI SUMMARY =====")
for k, v in kpi.items():
    print(f"{k:32}: {v}")

# ---------- 8. CORRELATION ANALYSIS ----------
corr = df[["Petrol_Price", "Diesel_Price", "Petrol_KL",
           "Diesel_KL", "Total_KL"]].corr().round(3)
print("\n===== CORRELATION MATRIX =====")
print(corr.to_string())
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f")
plt.title("Correlation Heatmap")
save("Correlation_Heatmap.png")

# ---------- 9. TREEMAP (optional) ----------
try:
    import squarify
    t = ranking.head(15)
    plt.figure(figsize=(12, 7))
    squarify.plot(sizes=t["Total_KL"],
                  label=[f"{d}\n{s}%" for d, s in zip(t["District"], t["Share_%"])],
                  color=sns.color_palette("viridis", len(t)), alpha=0.85,
                  text_kwargs={"fontsize": 9, "color": "white"})
    plt.axis("off"); plt.title("Treemap: Top 15 Districts by Consumption")
    save("Treemap.png")
except ImportError:
    print("\nTreemap skipped: run  pip install squarify")

# ---------- SAVE TABLES TO EXCEL ----------
with pd.ExcelWriter(os.path.join(BASE, "Advanced_Analysis_Output.xlsx")) as w:
    stats.to_excel(w, sheet_name="Statistics")
    yoy.to_excel(w, sheet_name="YoY_Growth")
    ranking.to_excel(w, sheet_name="District_Ranking", index=False)
    pd.DataFrame(kpi.items(), columns=["KPI", "Value"]).to_excel(
        w, sheet_name="KPI", index=False)
    corr.to_excel(w, sheet_name="Correlation")
print("\nDone! All charts and Advanced_Analysis_Output.xlsx saved.")