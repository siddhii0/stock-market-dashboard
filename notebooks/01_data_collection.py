# ============================================
# STEP 1 - Stock Market Data Collection
# Project: Indian Stock Market Dashboard
# Author: Siddhi Mishra
# ============================================

import yfinance as yf
import pandas as pd
import os

# --- Define the 5 stocks we want to analyze ---
stocks = {
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "Wipro": "WIPRO.NS"
}

# --- Set the date range (2 years of data) ---
start_date = "2023-01-01"
end_date   = "2025-01-01"

# --- Create the raw data folder if it doesn't exist ---
os.makedirs("../data/raw", exist_ok=True)

# --- Download and save each stock separately ---
for company_name, ticker in stocks.items():

    print(f"Downloading data for {company_name} ({ticker})...")

    # Download data from Yahoo Finance
    df = yf.download(ticker, start=start_date, end=end_date)

    # Add a column to identify the company
    df["Company"] = company_name
    df["Ticker"]  = ticker

    # Reset index so Date becomes a normal column
    df.reset_index(inplace=True)

    # Save to CSV in data/raw folder
    filename = f"../data/raw/{company_name.replace(' ', '_')}.csv"
    df.to_csv(filename, index=False)

    print(f"Saved {len(df)} rows to {filename}")

print("\n All 5 stocks downloaded successfully!")
print("Check your data/raw folder.")