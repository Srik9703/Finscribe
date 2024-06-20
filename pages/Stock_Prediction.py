import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# Function to preprocess and scale data
scaler = MinMaxScaler(feature_range=(0, 1))

def preprocess_data(ticker):
    df = yf.download(ticker, start='2010-01-01', end='2020-01-01')
    df = df[['Close']]
    return df

# Create dataset function for LSTM
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

# LSTM Model
def build_model():
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(100, 1)))
    model.add(LSTM(50, return_sequences=True))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

# Streamlit app
st.header("Stock Prediction")

# Input for company names
comp = st.multiselect("Enter 1 or more company names", options=["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"])
st.write("Selected companies:", comp)

# Input for number of days to predict
days_to_predict = st.number_input("Enter the number of days to predict:", min_value=1, value=30)

# Prediction button
if st.button("Predict"):
    if comp:
        company_data = []
        company_names = []

        # Preprocess and scale data
        for ticker in comp:
            df = preprocess_data(ticker)
            scaled_data = scaler.fit_transform(np.array(df).reshape(-1, 1))
            company_data.append(scaled_data)
            company_names.append(ticker)

        # Train and test split
        train_data_list = []
        test_data_list = []
        for data in company_data:
            training_size = int(len(data) * 0.65)
            train_data, test_data = data[0:training_size, :], data[training_size:len(data), :1]
            train_data_list.append(train_data)
            test_data_list.append(test_data)

        # Train the model
        model = build_model()
        time_step = 100
        for train_data in train_data_list:
            X_train, y_train = create_dataset(train_data, time_step)
            X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
            model.fit(X_train, y_train, epochs=7, batch_size=64, verbose=1)

        # Predict the stock prices
        result = []
        for i, test_data in enumerate(test_data_list):
            x_input = test_data[-time_step:].reshape(1, -1)
            temp_input = list(x_input)
            temp_input = temp_input[0].tolist()

            lst_output = []
            n_steps = time_step
            for _ in range(days_to_predict):
                if len(temp_input) > n_steps:
                    x_input = np.array(temp_input[1:])
                    x_input = x_input.reshape((1, n_steps, 1))
                    yhat = model.predict(x_input, verbose=0)
                    temp_input.extend(yhat[0].tolist())
                    temp_input = temp_input[1:]
                    lst_output.extend(yhat.tolist())
                else:
                    x_input = x_input.reshape((1, n_steps, 1))
                    yhat = model.predict(x_input, verbose=0)
                    temp_input.extend(yhat[0].tolist())
                    lst_output.extend(yhat.tolist())

            df = company_data[i].tolist()
            df.extend(lst_output)
            result.append(df)

      # Plot the results
        plt.figure(figsize=(10, 6))
        for i, graph in enumerate(result):
            plt.plot(graph, label=comp[i])
        plt.title('Stock Price Prediction')
        plt.xlabel('Time')
        plt.ylabel('Stock Price')
        plt.legend()
        st.pyplot(plt)
    else:
        st.write("Please select at least one company.")

