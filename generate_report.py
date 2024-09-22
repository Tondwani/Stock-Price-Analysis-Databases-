import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

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

# Simple trading strategy: Moving average crossover
df['Signal'] = 0
df['Signal'][df['MA50'] > df['MA200']] = 1
df['Signal'][df['MA50'] < df['MA200']] = -1

# Backtest the strategy
df['Position'] = df['Signal'].shift()
df['StrategyReturns'] = df['Returns'] * df['Position']

# Calculate performance metrics
cumulative_returns = (df['Returns'] + 1).cumprod()
cumulative_strategy_returns = (df['StrategyReturns'] + 1).cumprod()

plt.figure(figsize=(14, 7))
plt.plot(cumulative_returns, label='Buy and Hold')
plt.plot(cumulative_strategy_returns, label='Strategy')
plt.legend()
plt.title('Strategy Performance')
plt.show()

# Summary report
summary = {
    'Total Return': cumulative_returns[-1] - 1,
    'Strategy Return': cumulative_strategy_returns[-1] - 1,
    'Volatility': df['Volatility'].mean()
}

print("Summary Report:")
for key, value in summary.items():
    print(f"{key}: {value:.2%}")

