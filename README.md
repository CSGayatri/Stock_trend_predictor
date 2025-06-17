# 📈 Real-Time Stock Price Predictor

A web-based application to analyze and predict stock prices using historical data and machine learning models in real time. Built with **Streamlit**, it fetches live stock data using the **Alpha Vantage API**, visualizes trends, and applies ML models to forecast future prices.

👉 **Live Demo:** [https://stocktrendpredictor-uajqusepoqxnzfbjkdleav.streamlit.app/](https://stocktrendpredictor-uajqusepoqxnzfbjkdleav.streamlit.app/)
🧠 **Tech Stack:** Python, Streamlit, Scikit-learn, Pandas, Alpha Vantage API, Matplotlib

---

## 🚀 Features

- 🔍 Search and visualize real-time stock data
- 📉 View historical trends using line charts
- 🤖 Predict future stock prices using ML models:
  - Linear Regression
  - Random Forest Regressor
  - Gradient Boosting Regressor
  - Support Vector Regressor (SVR)
- 📊 Evaluate model performance with RMSE
- 📦 Download processed data as CSV

---

## 🛠️ Tech Stack

| Component         | Tech Used                   |
|------------------|-----------------------------|
| Frontend UI      | Streamlit                   |
| Data Source      | Alpha Vantage API           |
| ML Models        | Scikit-learn (sklearn)      |
| Data Handling    | Pandas, NumPy               |
| Visualization    | Matplotlib                  |
| Deployment       | Streamlit Share / Render / Local |

---

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/CSGayatri/real-time-stock-predictor.git
cd real-time-stock-predictor

2. Install Dependencies
It's recommended to use a virtual environment:
pip install -r requirements.txt

3. Add API Key
Create a .env file in the root directory:
ALPHA_VANTAGE_API_KEY=your_api_key_here

4. Run the App
streamlit run app.py

🔐 Environment Variables
If you're using environment variables, ensure .env contains:
ALPHA_VANTAGE_API_KEY=your_key

And load it in your code using:
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
