import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

# Alpha Vantage API Key
API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"

# Company Tickers
companies = {
    "Google (Alphabet)": "GOOGL",
    "Microsoft": "MSFT",
    "Apple": "AAPL",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Tesla": "TSLA",
    "Meta": "META",
    "IBM": "IBM",
    "Intel": "INTC",
    "AMD": "AMD",
}

# Fetch stock data using Alpha Vantage
@st.cache_data
def fetch_stock_data(ticker):
    ts = TimeSeries(key=API_KEY, output_format="pandas")
    try:
        data, meta_data = ts.get_daily(symbol=ticker, outputsize="compact")
        data = data.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        })
        data["Date"] = data.index
        data = data.sort_index(ascending=True)  # Ensure correct order
        return data.reset_index(drop=True)
    except Exception as e:
        return None  # Return None on failure

# Calculate technical indicators
def calculate_indicators(data):
    # Simple Moving Average (SMA)
    data["SMA_20"] = data["Close"].rolling(window=20).mean()
    
    # Exponential Moving Average (EMA)
    data["EMA_20"] = data["Close"].ewm(span=20, adjust=False).mean()

    # Bollinger Bands
    rolling_std = data["Close"].rolling(window=20).std()
    data["Upper_Band"] = data["SMA_20"] + (rolling_std * 2)
    data["Lower_Band"] = data["SMA_20"] - (rolling_std * 2)

    # Relative Strength Index (RSI)
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data["RSI"] = 100 - (100 / (1 + rs))

    # MACD and Signal Line
    data["MACD"] = data["Close"].ewm(span=12, adjust=False).mean() - data["Close"].ewm(span=26, adjust=False).mean()
    data["MACD_Signal"] = data["MACD"].ewm(span=9, adjust=False).mean()

    # Average Directional Index (ADX)
    high_low = data["High"] - data["Low"]
    high_close = abs(data["High"] - data["Close"].shift())
    low_close = abs(data["Low"] - data["Close"].shift())
    tr = high_low.combine(high_close, max).combine(low_close, max)
    atr = tr.rolling(window=14).mean()
    data["ADX"] = atr

    # On-Balance Volume (OBV)
    data["OBV"] = (np.sign(data["Close"].diff()) * data["Volume"]).fillna(0).cumsum()

    return data.dropna()

# Stock price prediction
def stock_price_prediction(data, model_type="Linear Regression"):
    features = ["SMA_20", "EMA_20", "RSI", "MACD", "ADX"]
    data = data.dropna()

    X = data[features]  # Features
    y = data["Close"]  # Target variable

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Select model
    if model_type == "Linear Regression":
        model = LinearRegression()
    elif model_type == "Random Forest":
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    elif model_type == "Support Vector Machine":
        model = SVR(kernel="rbf")
    elif model_type == "Gradient Boosting":
        model = GradientBoostingRegressor(n_estimators=100, random_state=42)

    model.fit(X_scaled, y)
    
    # Predict next day's price
    predicted_price = model.predict(X_scaled[-1:].reshape(1, -1))
    mse = mean_squared_error(y, model.predict(X_scaled))

    return predicted_price[0], mse

# Streamlit App Layout
st.title("📈 Real-Time Stock Price Tracker & Prediction")

# Sidebar - Stock selection
st.sidebar.header("Stock Selection")
selected_company = st.sidebar.selectbox("Select a company:", companies.keys())
selected_ticker = companies[selected_company]

# Fetch stock data
data = fetch_stock_data(selected_ticker)

# Check if data is available
if data is None or data.empty:
    st.error("❌ No stock data available. Check API key or stock symbol.")
else:
    st.success(f"✅ Data loaded for {selected_company}")

    # Calculate technical indicators
    data = calculate_indicators(data)

    # Display current price
    if not data.empty:
        current_price = data["Close"].iloc[-1]
        st.sidebar.write(f"💰 **Current Price**: ${current_price:.2f}")

        # Select prediction model
        model_type = st.sidebar.selectbox(
            "Select Prediction Model:",
            ["Linear Regression", "Random Forest", "Support Vector Machine", "Gradient Boosting"]
        )

        # Predict stock price
        predicted_price, mse_price = stock_price_prediction(data, model_type)
        st.sidebar.write(f"🔮 **Predicted Next Day Price**: ${predicted_price:.2f}")
        st.sidebar.write(f"📉 **Model MSE**: {mse_price:.4f}")

        # Plot stock prices and indicators
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(data["Date"], data["Close"], label="Close Price", color="black", lw=1.5)
        ax.plot(data["Date"], data["SMA_20"], label="SMA 20", color="blue", lw=1)
        ax.plot(data["Date"], data["EMA_20"], label="EMA 20", color="red", lw=1)
        ax.fill_between(data["Date"], data["Lower_Band"], data["Upper_Band"], color="magenta", alpha=0.1, label="Bollinger Bands")

        # Buy/Sell Signals
        ax.scatter(data["Date"][data["MACD"] > data["MACD_Signal"]], data["Close"][data["MACD"] > data["MACD_Signal"]],
                   marker="^", color="green", label="Buy Signal", zorder=5)
        ax.scatter(data["Date"][data["MACD"] < data["MACD_Signal"]], data["Close"][data["MACD"] < data["MACD_Signal"]],
                   marker="v", color="red", label="Sell Signal", zorder=5)

        ax.set_title(f"{selected_company} Stock Price & Indicators")
        ax.set_xlabel("Date")
        ax.set_ylabel("Stock Price (USD)")
        ax.legend()
        ax.grid()
        st.pyplot(fig)
