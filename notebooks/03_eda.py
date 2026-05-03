# ============================================
# STEP 3 - Exploratory Data Analysis (EDA)
# Project: Indian Stock Market Dashboard
# Author: Siddhi Mishra
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import os

# --- Create folder to save charts ---
os.makedirs("../dashboard/charts", exist_ok=True)

# --- Load master cleaned data ---
df = pd.read_csv("../data/cleaned/all_stocks_master.csv")
df["Date"] = pd.to_datetime(df["Date"])

companies = ["Reliance", "TCS", "HDFC Bank", "Infosys", "Wipro"]
colors    = ["#2196F3", "#4CAF50", "#FF5722", "#9C27B0", "#FF9800"]

print("Data loaded successfully!")
print(f"Shape: {df.shape}")

# ============================================
# CHART 1 - Closing Price Trends
# ============================================

print("\nGenerating Chart 1 - Closing Price Trends...")

fig, ax = plt.subplots(figsize=(14, 6))

for company, color in zip(companies, colors):
    data = df[df["Company"] == company]
    ax.plot(data["Date"], data["Close"], label=company, color=color, linewidth=1.5)

ax.set_title("Closing Price Trends - 5 Indian Stocks (2023-2024)", fontsize=14, fontweight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Price (INR)")
ax.legend()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../dashboard/charts/01_closing_price_trends.png", dpi=150)
plt.close()
print("  Saved: 01_closing_price_trends.png")

# ============================================
# CHART 2 - Moving Averages (Reliance example)
# ============================================

print("\nGenerating Chart 2 - Moving Averages...")

reliance = df[df["Company"] == "Reliance"].copy()
reliance["MA30"] = reliance["Close"].rolling(window=30).mean()
reliance["MA90"] = reliance["Close"].rolling(window=90).mean()

# Save moving averages back to cleaned data
for company in companies:
    mask = df["Company"] == company
    df.loc[mask, "MA30"] = df.loc[mask, "Close"].rolling(window=30).mean()
    df.loc[mask, "MA90"] = df.loc[mask, "Close"].rolling(window=90).mean()

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(reliance["Date"], reliance["Close"], label="Close Price", color="#2196F3", linewidth=1)
ax.plot(reliance["Date"], reliance["MA30"],  label="30-Day MA",   color="#FF9800", linewidth=1.5)
ax.plot(reliance["Date"], reliance["MA90"],  label="90-Day MA",   color="#F44336", linewidth=1.5)
ax.set_title("Reliance - Close Price vs Moving Averages", fontsize=14, fontweight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Price (INR)")
ax.legend()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../dashboard/charts/02_moving_averages.png", dpi=150)
plt.close()
print("  Saved: 02_moving_averages.png")

# ============================================
# CHART 3 - Daily % Returns
# ============================================

print("\nGenerating Chart 3 - Daily Returns...")

for company in companies:
    mask = df["Company"] == company
    df.loc[mask, "Daily_Return"] = df.loc[mask, "Close"].pct_change() * 100

fig, axes = plt.subplots(5, 1, figsize=(14, 16), sharex=True)

for i, (company, color) in enumerate(zip(companies, colors)):
    data = df[df["Company"] == company]
    axes[i].plot(data["Date"], data["Daily_Return"], color=color, linewidth=0.8, alpha=0.8)
    axes[i].axhline(y=0, color="black", linewidth=0.5, linestyle="--")
    axes[i].set_title(company, fontsize=11, fontweight="bold")
    axes[i].set_ylabel("Return %")

plt.suptitle("Daily % Returns - All Stocks (2023-2024)", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("../dashboard/charts/03_daily_returns.png", dpi=150)
plt.close()
print("  Saved: 03_daily_returns.png")

# ============================================
# CHART 4 - Volatility (30-day rolling std)
# ============================================

print("\nGenerating Chart 4 - Volatility...")

fig, ax = plt.subplots(figsize=(14, 6))

for company, color in zip(companies, colors):
    mask = df["Company"] == company
    df.loc[mask, "Volatility"] = df.loc[mask, "Daily_Return"].rolling(window=30).std()
    data = df[df["Company"] == company]
    ax.plot(data["Date"], data["Volatility"], label=company, color=color, linewidth=1.5)

ax.set_title("30-Day Rolling Volatility - All Stocks", fontsize=14, fontweight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Volatility (Std Dev of Daily Returns)")
ax.legend()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../dashboard/charts/04_volatility.png", dpi=150)
plt.close()
print("  Saved: 04_volatility.png")

# ============================================
# CHART 5 - Correlation Heatmap
# ============================================

print("\nGenerating Chart 5 - Correlation Heatmap...")

pivot = df.pivot_table(index="Date", columns="Company", values="Close")
correlation = pivot.corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation, annot=True, fmt=".2f", cmap="RdYlGn",
            vmin=-1, vmax=1, ax=ax, linewidths=0.5)
ax.set_title("Stock Price Correlation Matrix", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("../dashboard/charts/05_correlation_heatmap.png", dpi=150)
plt.close()
print("  Saved: 05_correlation_heatmap.png")

# ============================================
# SAVE UPDATED MASTER CSV WITH NEW COLUMNS
# ============================================

df.to_csv("../data/cleaned/all_stocks_master.csv", index=False)
print("\nMaster CSV updated with MA30, MA90, Daily_Return, Volatility columns")

# ============================================
# PRINT KEY FINDINGS
# ============================================

print("\n" + "="*50)
print("KEY FINDINGS")
print("="*50)

# Best performer
returns = df.groupby("Company")["Daily_Return"].mean().sort_values(ascending=False)
print(f"\nAverage Daily Return (best to worst):")
for company, ret in returns.items():
    print(f"  {company}: {ret:.4f}%")

# Most volatile
vol = df.groupby("Company")["Daily_Return"].std().sort_values(ascending=False)
print(f"\nMost Volatile Stock: {vol.index[0]} (std: {vol.iloc[0]:.4f}%)")
print(f"Least Volatile Stock: {vol.index[-1]} (std: {vol.iloc[-1]:.4f}%)")

print("\nEDA Complete! Check dashboard/charts folder for all 5 charts.")