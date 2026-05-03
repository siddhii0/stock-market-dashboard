# ============================================
# STEP 2 - Data Cleaning & Preprocessing
# Project: Indian Stock Market Dashboard
# Author: Siddhi Mishra
# ============================================

import pandas as pd
import os

# --- Create cleaned folder if it doesn't exist ---
os.makedirs("../data/cleaned", exist_ok=True)

# --- List of all stock files ---
stocks = ["Reliance", "TCS", "HDFC_Bank", "Infosys", "Wipro"]

# --- Load and clean each file ---
all_stocks = []

for stock in stocks:

    print(f"Cleaning {stock} data...")

    # Load the raw CSV
    df = pd.read_csv(f"../data/raw/{stock}.csv")

    # Check for missing values
    print(f"  Missing values before cleaning: {df.isnull().sum().sum()}")

    # Drop rows where Close price is missing
    df.dropna(subset=["Close"], inplace=True)

    # Check for duplicates
    df.drop_duplicates(inplace=True)

    # Make sure Date column is proper date format
    df["Date"] = pd.to_datetime(df["Date"])

    # Keep only the columns we need
    df = df[["Date", "Open", "High", "Low", "Close", "Volume", "Company", "Ticker"]]

    # Sort by date
    df.sort_values("Date", inplace=True)

    # Reset index
    df.reset_index(drop=True, inplace=True)

    print(f"  Rows after cleaning: {len(df)}")
    print(f"  Date range: {df['Date'].min()} to {df['Date'].max()}")

    # Save individual cleaned file
    df.to_csv(f"../data/cleaned/{stock}_cleaned.csv", index=False)

    # Add to master list
    all_stocks.append(df)

# --- Combine all 5 stocks into one master dataframe ---
# --- Combine all 5 stocks into one master dataframe ---
print("\nCombining all stocks into master file...")
master_df = pd.concat(all_stocks, ignore_index=True)

# --- Remove any rows where Company name is missing ---
master_df.dropna(subset=["Company"], inplace=True)
master_df.reset_index(drop=True, inplace=True)

# --- Save master file ---
master_df.to_csv("../data/cleaned/all_stocks_master.csv", index=False)

print(f"\nMaster file created with {len(master_df)} total rows")
print(f"Companies included: {master_df['Company'].unique()}")
print("\nAll stocks cleaned successfully!")