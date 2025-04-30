📈 Real-Time Stock Price Tracker & Prediction
This is a powerful and interactive web app built with Streamlit that allows users to:

Track real-time stock data using the Alpha Vantage API

Visualize key technical indicators (SMA, EMA, RSI, Bollinger Bands, MACD, etc.)

Predict the next day's stock price using machine learning models like:

Linear Regression

Random Forest

Support Vector Machine (SVM)

Gradient Boosting

🚀 Features
📊 Real-time stock data for top companies (Apple, Tesla, Microsoft, etc.)

🧠 ML-based price prediction with error metrics (MSE)

📈 Interactive plots with buy/sell signal highlights

🔍 Multiple model selection for better insights

🛠️ Technologies Used
Streamlit – For building the UI

Alpha Vantage API – For fetching stock market data

Pandas / NumPy – Data manipulation

Matplotlib – Data visualization

Scikit-learn – Machine learning (regression models and preprocessing)

📦 Installation
Clone the repo

bash
Copy
Edit
git clone https://github.com/CSGayatri/stock-predictor-app.git
cd stock-predictor-app
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Get an Alpha Vantage API key

Sign up at Alpha Vantage and get your free API key.

Replace the placeholder in the code:

python
Copy
Edit
API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"
▶️ Run the App
bash
Copy
Edit
streamlit run app.py
🧠 ML Models Used
Linear Regression – Simple linear fit

Random Forest Regressor – Ensemble method for robust predictions

Support Vector Regression (SVR) – Kernel-based regression

Gradient Boosting Regressor – High-performance boosting model

Each model is evaluated using Mean Squared Error (MSE).


📌 Notes
Some features like MACD/RSI calculations require historical data, so results may vary based on the "compact" vs "full" data returned by Alpha Vantage.

Be mindful of Alpha Vantage's API call limits (5 calls/min and 500/day for free tier).

📄 License
MIT License. Feel free to use, modify, and contribute!

