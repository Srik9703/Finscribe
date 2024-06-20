import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Function to fetch historical data and calculate daily returns
def fetch_and_calculate_returns(ticker1, ticker2):
    # Fetch historical data from Yahoo Finance
    data1 = yf.download(ticker1, start='2020-01-01', end='2024-06-13')['Adj Close']
    data2 = yf.download(ticker2, start='2020-01-01', end='2024-06-13')['Adj Close']
    
    # Calculate daily returns
    returns1 = data1.pct_change() * 100
    returns2 = data2.pct_change() * 100
    
    # Combine into a DataFrame
    df = pd.DataFrame({'Stock1': returns1, 'Stock2': returns2})
    
    return df.dropna()

# Streamlit app
st.title("Stock Daily Returns Comparison")

# Input for ticker symbols
ticker1 = st.text_input("Enter the first ticker symbol:", "MSFT")
ticker2 = st.text_input("Enter the second ticker symbol (or ^GSPC for S&P 500):", "^GSPC")

if st.button("Fetch and Compare Returns"):
    try:
        # Fetch data and calculate returns
        df_returns = fetch_and_calculate_returns(ticker1, ticker2)
        
        # Plotting the scatter plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(df_returns['Stock1'], df_returns['Stock2'], alpha=0.8)
        ax.set_title(f'Daily Returns Comparison: {ticker1} vs {ticker2}')
        ax.set_xlabel(f'Daily Returns {ticker1} (%)')
        ax.set_ylabel(f'Daily Returns {ticker2} (%)')
        ax.grid(True)
        plt.tight_layout()
        
        # Display the plot in Streamlit
        st.pyplot(fig)
        
        # Display correlation coefficient
        correlation = df_returns.corr().iloc[0, 1]
        st.write(f"Correlation coefficient between {ticker1} and {ticker2}: {correlation:.2f}")

        # Analysis
        if correlation > 0.7:
            st.write("The stocks are strongly positively correlated.")
        elif correlation > 0.3:
            st.write("The stocks are moderately positively correlated.")
        elif correlation > -0.3:
            st.write("The stocks have little to no correlation.")
        elif correlation > -0.7:
            st.write("The stocks are moderately negatively correlated.")
        else:
            st.write("The stocks are strongly negatively correlated.")

        # Display the first few rows of the data for reference
        st.write("First few rows of the daily returns data:")
        st.dataframe(df_returns.head())
    except Exception as e:
        st.write(f"An error occurred: {e}")
