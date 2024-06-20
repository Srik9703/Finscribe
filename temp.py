import requests
import pandas as pd
import streamlit as st 
api_url = f"https://discountingcashflows.com/api/prices/daily/AAPL/"
response = requests.get(api_url)
data = response.json()

# Create a DataFrame
df2= pd.DataFrame(data['report'])
print(df2.head(20))
df=df2.head(20)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Calculate daily returns
df['daily_return'] = df['close'].pct_change()

# Calculate rolling standard deviation of daily returns for last 20 days
rolling_std_20 = df['daily_return'].rolling(window=20).std()

# Display rolling standard deviation plot
st.title("Rolling Standard Deviation of Daily Returns for Last 20 Days")
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(rolling_std_20.index, rolling_std_20, label='Rolling Std (20 days)')
ax.set_xlabel('Date')
ax.set_ylabel('Standard Deviation')
ax.legend()
ax.grid(True)

# Display plot in Streamlit
st.pyplot(fig)
