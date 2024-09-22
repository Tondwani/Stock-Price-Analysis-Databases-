import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('stock_data.db')

# Read data from the database
df = pd.read_sql_query("SELECT * FROM stock_prices", conn)

# Calculate basic statistics
df['Date'] = pd.to_datetime(df['date'])
df.set_index('Date', inplace=True)
df['Returns'] = df['close'].pct_change()
df['Volatility'] = df['Returns'].rolling(window=30).std() * (252**0.5)  # Annualized volatility
df['MA50'] = df['close'].rolling(window=50).mean()
df['MA200'] = df['close'].rolling(window=200).mean()

conn.close()

print("Data analysis complete!")
