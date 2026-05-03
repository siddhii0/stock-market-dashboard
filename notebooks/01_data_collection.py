# ============================================================
# STEP 1: Fetch Indian Stock Data using yfinance
# Project: Indian Stock Market Analysis
# File: 01_fetch_data.py
# ============================================================

# --- Import libraries ---
import yfinance as yf          # for downloading stock data from Yahoo Finance
import pandas as pd            # for data manipulation and saving CSVs
import os                      # for creating folders
from datetime import datetime, timedelta  # for calculating date ranges

# ============================================================
# CONFIGURATION — edit this section if you want to change
# the stocks or time period
# ============================================================

# Dictionary of company names mapped to their NSE ticker symbols
# NSE tickers on Yahoo Finance always end with ".NS"
STOCKS = {
    "Reliance":  "RELIANCE.NS",
    "TCS":       "TCS.NS",
    "HDFC_Bank": "HDFCBANK.NS",
    "Infosys":   "INFY.NS",
    "Wipro":     "WIPRO.NS",
}

# Set the date range: today going back 2 years (730 days)
END_DATE   = datetime.today().strftime("%Y-%m-%d")        # today's date as string
START_DATE = (datetime.today() - timedelta(days=730)).strftime("%Y-%m-%d")

# Folder where raw CSVs will be saved
OUTPUT_DIR = "data/raw"

# ============================================================
# SETUP — create the output folder if it doesn't exist
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)  # exist_ok=True means no error if folder exists
print(f"Output folder ready: {OUTPUT_DIR}")
print(f"Fetching data from {START_DATE} to {END_DATE}\n")

# ============================================================
# FETCH LOOP — download data for each stock one by one
# ============================================================

for company_name, ticker_symbol in STOCKS.items():

    print(f"Downloading: {company_name} ({ticker_symbol}) ...", end=" ")

    # Download OHLCV data from Yahoo Finance
    # auto_adjust=True adjusts prices for stock splits and dividends automatically
    df = yf.download(
        ticker_symbol,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=True,   # adjusts for splits & dividends (best practice)
        progress=False      # hides the download progress bar for cleaner output
    )

    # --- Check if data was actually returned ---
    if df.empty:
        print(f"WARNING: No data found for {ticker_symbol}. Skipping.")
        continue  # skip to the next stock if this one fails

    # --- Flatten multi-level column headers (yfinance sometimes returns them) ---
    # yfinance can return columns like ('Close', 'RELIANCE.NS') — flatten to just 'Close'
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # --- Keep only the 5 columns we need: Open, High, Low, Close, Volume ---
    df = df[["Open", "High", "Low", "Close", "Volume"]]

    # --- Reset the index so 'Date' becomes a regular column (not the row label) ---
    # This makes it easier to work with in pandas and Power BI later
    df.reset_index(inplace=True)

    # --- Rename the index column to 'Date' explicitly for clarity ---
    df.rename(columns={"index": "Date", "Datetime": "Date"}, inplace=True)

    # --- Ensure the Date column is in datetime format ---
    df["Date"] = pd.to_datetime(df["Date"])

    # --- Add a column to identify which company this data belongs to ---
    # Useful when we merge all stocks in Step 2
    df["Company"]  = company_name
    df["Ticker"]   = ticker_symbol

    # --- Round all price columns to 2 decimal places (cleaner CSVs) ---
    for col in ["Open", "High", "Low", "Close"]:
        df[col] = df[col].round(2)

    # --- Build the output file path ---
    # e.g., data/raw/Reliance_raw.csv
    output_path = os.path.join(OUTPUT_DIR, f"{company_name}_raw.csv")

    # --- Save to CSV ---
    # index=False means don't write row numbers (0, 1, 2...) into the CSV
    df.to_csv(output_path, index=False)

    print(f"Saved {len(df)} rows → {output_path}")

# ============================================================
# DONE — print a summary
# ============================================================

print("\n" + "="*50)
print("All stocks downloaded successfully!")
print(f"CSVs saved in: {OUTPUT_DIR}/")
print("="*50)

# --- Quick preview: read back one file to verify it looks correct ---
sample_path = os.path.join(OUTPUT_DIR, "Reliance_raw.csv")
sample_df = pd.read_csv(sample_path)

print(f"\nPreview of Reliance_raw.csv ({sample_df.shape[0]} rows × {sample_df.shape[1]} cols):")
print(sample_df.head())             # show first 5 rows
print("\nColumn data types:")
print(sample_df.dtypes)             # verify Date is datetime, numbers are float
print("\nBasic statistics:")
print(sample_df[["Open", "High", "Low", "Close", "Volume"]].describe().round(2))