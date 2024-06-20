import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.title("Volatility Exploration")
company_ticker_symbol = {
    "Apple Inc.": "AAPL",
    "Microsoft Corporation": "MSFT",
    "Amazon.com Inc.": "AMZN",
    "Alphabet Inc. (Class A)": "GOOGL",
    "Alphabet Inc. (Class C)": "GOOG",
    "Facebook, Inc.": "META",
    "Tesla, Inc.": "TSLA",
    "Berkshire Hathaway Inc.": "BRK.A",
    "Johnson & Johnson": "JNJ",
    "JPMorgan Chase & Co.": "JPM",
    "Visa Inc.": "V",
    "Procter & Gamble Co.": "PG",
    "NVIDIA Corporation": "NVDA",
    "Walmart Inc.": "WMT",
    "Mastercard Incorporated": "MA",
    "The Walt Disney Company": "DIS",
    "PayPal Holdings, Inc.": "PYPL",
    "Adobe Inc.": "ADBE",
    "Netflix, Inc.": "NFLX",
    "Comcast Corporation": "CMCSA",
    "Cisco Systems, Inc.": "CSCO",
    "Exxon Mobil Corporation": "XOM",
    "PepsiCo, Inc.": "PEP",
    "Coca-Cola Company": "KO",
    "Pfizer Inc.": "PFE",
    "Intel Corporation": "INTC",
    "Nike, Inc.": "NKE",
    "Oracle Corporation": "ORCL",
    "Verizon Communications Inc.": "VZ",
    "AT&T Inc.": "T",
    "AbbVie Inc.": "ABBV",
    "Merck & Co., Inc.": "MRK",
    "Chevron Corporation": "CVX",
    "McDonald's Corporation": "MCD",
    "Salesforce.com Inc.": "CRM",
    "The Home Depot, Inc.": "HD",
    "International Business Machines Corporation": "IBM",
    "UnitedHealth Group Incorporated": "UNH",
    "Boeing Company": "BA",
    "Qualcomm Incorporated": "QCOM"
}

# Function to calculate rolling standard deviation and return data for plotting
def calculate_rolling_std(data, days):
    # Create DataFrame from API response data
    df = pd.DataFrame(data['report'])

    # Convert 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Sort DataFrame by 'date' in ascending order (just in case it's not sorted)
    df.sort_values(by='date', ascending=True, inplace=True)

    # Calculate daily returns
    df['daily_return'] = df['close'].pct_change()

    # Calculate rolling standard deviation of daily returns
    df['rolling_std'] = df['daily_return'].rolling(window=days).std()

    # Prepare data for plotting
    chart_data = df[['date', 'rolling_std']].set_index('date').tail(days)

    return chart_data

# Streamlit app code
st.subheader("Rolling Standard Deviation of Daily Returns")

# Selection box for company name
companies = list(company_ticker_symbol.keys())
st.subheader("Select company name:")

select = st.selectbox("Company name", options=companies)

# Number of days input
days = st.slider("Select number of days for rolling standard deviation:", min_value=1, max_value=30, value=3)

# Fetch data from the API
api_url = f"https://discountingcashflows.com/api/prices/daily/{company_ticker_symbol[select]}/"
response = requests.get(api_url)
data = response.json()

# Check if data is fetched successfully
if 'report' in data:
    # Calculate rolling standard deviation and get data for plotting
    chart_data = calculate_rolling_std(data, days)

    # Plot using st.line_chart
    st.line_chart(chart_data)
    st.write("")
    
else:
    st.error("Failed to fetch data. Please try again later.")
