import streamlit as st

import yfinance as yf
 
#Simple Moving Average of a company
def calculate_SMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.rolling(window=window).mean().iloc[-1])

#Exponential Moving Average of a company
def calculate_EMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    return str(data.ewm(span=window, adjust=False).mean().iloc[-1])

#Relative Strength Index of a company
def calculate_RSI(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    delta = data.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=13, adjust=False).mean()
    ema_down = down.ewm(com=13, adjust=False).mean()
    rs = ema_up / ema_down
    return str(100 - (100 / (1 + rs.iloc[-1])))

#Moving Average Convergence Divergence of a company g
def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    ema_12 = data.ewm(span=12, adjust=False).mean()
    ema_26 = data.ewm(span=26, adjust=False).mean()
    MACD = ema_12 - ema_26
    signal = MACD.ewm(span=9, adjust=False).mean()
    MACD_histogram = MACD - signal
    return f"{MACD.iloc[-1]}, {signal.iloc[-1]}, {MACD_histogram.iloc[-1]}"

# Streamlit app
st.title("Stock Technical Indicators")

# Input for ticker symbol
ticker = st.text_input("Enter the ticker symbol:")

# Input for SMA and EMA window size
window = st.number_input("Enter the window size for SMA and EMA:", min_value=1, value=20)

if st.button("Calculate Indicators"):
    if ticker:
        try:
            # Calculate and display SMA
            sma = calculate_SMA(ticker, window)
            st.write(f"SMA({window}): {sma}")

            # Calculate and display EMA
            ema = calculate_EMA(ticker, window)
            st.write(f"EMA({window}): {ema}")

            # Calculate and display RSI
            rsi = calculate_RSI(ticker)
            st.write(f"RSI: {rsi}")

            # Calculate and display MACD
            macd, signal, macd_histogram = calculate_MACD(ticker).split(', ')
            st.write(f"MACD: {macd}")
            #st.write(f"Signal Line: {signal}")
            #st.write(f"MACD Histogram: {macd_histogram}")
        except Exception as e:
            st.write(f"An error occurred: {e}")
    else:
        st.write("Please enter a ticker symbol.")
