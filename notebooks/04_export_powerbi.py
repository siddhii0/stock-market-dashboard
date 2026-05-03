# ============================================
# STEP 4 - Export Clean CSVs for Power BI
# Project: Indian Stock Market Dashboard
# Author: Siddhi Mishra
# ============================================

import pandas as pd
import os

os.makedirs("../data/powerbi", exist_ok=True)

# --- Load master data ---
df = pd.read_csv("../data/cleaned/all_stocks_master.csv")
df["Date"] = pd.to_datetime(df["Date"])

print("Data loaded!")
print(f"Columns available: {df.columns.tolist()}")

# ============================================
# EXPORT 1 - Daily Prices + Moving Averages
# (For line charts in Power BI)
# ============================================

export1 = df[["Date", "Company", "Open", "High", "Low", 
              "Close", "Volume", "MA30", "MA90"]].copy()

export1["Date"] = export1["Date"].dt.strftime("%Y-%m-%d")

export1.to_csv("../data/powerbi/01_daily_prices.csv", index=False)
print(f"\nExport 1 saved: 01_daily_prices.csv ({len(export1)} rows)")

# ============================================
# EXPORT 2 - Monthly Returns Summary
# (For monthly return bar chart / heatmap)
# ============================================

df["Year"]  = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.strftime("%b %Y")

monthly = df.groupby(["Company", "Year", "Month", "Month_Name"]).agg(
    Open      = ("Open",  "first"),
    Close     = ("Close", "last"),
    Avg_Volume= ("Volume","mean")
).reset_index()

monthly["Monthly_Return_%"] = ((monthly["Close"] - monthly["Open"]) / monthly["Open"] * 100).round(2)
monthly = monthly.sort_values(["Company", "Year", "Month"])

monthly.to_csv("../data/powerbi/02_monthly_returns.csv", index=False)
print(f"Export 2 saved: 02_monthly_returns.csv ({len(monthly)} rows)")

# ============================================
# EXPORT 3 - Performance Summary Table
# (For KPI cards and comparison bar chart)
# ============================================

summary = df.groupby("Company").agg(
    Start_Price    = ("Close", "first"),
    End_Price      = ("Close", "last"),
    Max_Price      = ("Close", "max"),
    Min_Price      = ("Close", "min"),
    Avg_Daily_Return = ("Daily_Return", "mean"),
    Volatility     = ("Daily_Return", "std"),
    Total_Trading_Days = ("Close", "count")
).reset_index()

summary["Total_Return_%"] = ((summary["End_Price"] - summary["Start_Price"]) 
                              / summary["Start_Price"] * 100).round(2)

summary["Avg_Daily_Return"] = summary["Avg_Daily_Return"].round(4)
summary["Volatility"]       = summary["Volatility"].round(4)
summary["Start_Price"]      = summary["Start_Price"].round(2)
summary["End_Price"]        = summary["End_Price"].round(2)

summary = summary.sort_values("Total_Return_%", ascending=False)

summary.to_csv("../data/powerbi/03_performance_summary.csv", index=False)
print(f"Export 3 saved: 03_performance_summary.csv ({len(summary)} rows)")

# ============================================
# PRINT FINAL SUMMARY
# ============================================

print("\n" + "="*55)
print("PERFORMANCE SUMMARY TABLE")
print("="*55)
print(summary[["Company", "Start_Price", "End_Price", 
               "Total_Return_%", "Volatility"]].to_string(index=False))

print("\n✅ All 3 Power BI CSVs exported to data/powerbi/")
print("\nNext step: Open Power BI Desktop and load these 3 files!")