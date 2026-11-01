import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

base = Path(__file__).parent
out = base / "charts"
out.mkdir(exist_ok=True)

yearly = pd.read_excel(base / "Yearly_Analysis.xlsx")
print(yearly)

years = yearly["Year"].astype(str)

# 1. Line chart: Petrol vs Diesel
plt.figure(figsize=(8, 5))
plt.plot(years, yearly["Petrol_Consumption"], marker="o", label="Petrol")
plt.plot(years, yearly["Diesel_Consumption"], marker="o", label="Diesel")
plt.title("Petrol vs Diesel Consumption")
plt.xlabel("Year")
plt.ylabel("Consumption (KL)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(out / "1_Petrol_vs_Diesel.png", dpi=150)

# 2. Bar chart: total per year
plt.figure(figsize=(8, 5))
bars = plt.bar(years, yearly["Total_Fuel_Consumption"], color="steelblue")
plt.bar_label(bars, fmt="%d", fontsize=8)
plt.title("Total Fuel Consumption by Year")
plt.xlabel("Year")
plt.ylabel("Consumption (KL)")
plt.tight_layout()
plt.savefig(out / "2_Total_by_Year.png", dpi=150)

# 3. Grouped bars
x = range(len(yearly))
w = 0.4
plt.figure(figsize=(8, 5))
plt.bar([i - w / 2 for i in x], yearly["Petrol_Consumption"], w, label="Petrol", color="orange")
plt.bar([i + w / 2 for i in x], yearly["Diesel_Consumption"], w, label="Diesel", color="seagreen")
plt.xticks(list(x), years)
plt.title("Petrol and Diesel Consumption by Year")
plt.xlabel("Year")
plt.ylabel("Consumption (KL)")
plt.legend()
plt.tight_layout()
plt.savefig(out / "3_Grouped_Bar.png", dpi=150)

# 4. Pie chart: share
plt.figure(figsize=(6, 6))
totals = [yearly["Petrol_Consumption"].sum(), yearly["Diesel_Consumption"].sum()]
plt.pie(totals, labels=["Petrol", "Diesel"], autopct="%1.1f%%",
        colors=["orange", "seagreen"], startangle=90)
plt.title("Share of Petrol and Diesel")
plt.tight_layout()
plt.savefig(out / "4_Share_Pie.png", dpi=150)

# 5. Year-on-year growth
growth = yearly["Total_Fuel_Consumption"].pct_change() * 100
plt.figure(figsize=(8, 5))
plt.plot(years[1:], growth[1:], marker="o", color="crimson")
plt.title("Year-on-Year Growth in Total Fuel Consumption")
plt.xlabel("Year")
plt.ylabel("Growth (%)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(out / "5_YoY_Growth.png", dpi=150)

plt.show()