import yfinance as yf
import sqlite3
import pandas as pd
import os

# Define the list of stock symbols
stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'BRK-B', 'JNJ', 'V', 'WMT']

# Download historical data for the past 5 years
data = {}
for stock in stocks:
    data[stock] = yf.download(stock, start="2019-01-01", end="2024-01-01")

# Delete the existing database file if it exists
if os.path.exists('stock_data.db'):
    os.remove('stock_data.db')

# Connect to SQLite database
conn = sqlite3.connect('stock_data.db')
c = conn.cursor()

# Create table schema
c.execute('''
CREATE TABLE IF NOT EXISTS stock_prices (
    id INTEGER PRIMARY KEY,
    symbol TEXT,
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    adj_close REAL,
    volume INTEGER
)
''')

# Insert data into the database
for stock, df in data.items():
    df['symbol'] = stock
    df.reset_index(inplace=True)
    df = df.rename(columns={
        'Date': 'date',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Adj Close': 'adj_close',
        'Volume': 'volume'
    })
    df[['symbol', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']].to_sql('stock_prices', conn, if_exists='append', index=False)

conn.commit()
conn.close()

print("Data collection and database insertion complete!")
