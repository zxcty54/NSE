from flask import Flask, request, jsonify
import yfinance as yf
from flask_cors import CORS
import threading
import time
import json
import os

app = Flask(__name__)
CORS(app)

JSON_FILE = "prices.json"

# **Load Cached Prices**
def load_prices():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    return {}

# **Save Prices to JSON**
def save_prices(data):
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

# **Fetch Stock Prices Every 15 Sec**
def fetch_stock_prices():
    while True:
        try:
            stored_prices = load_prices()  # Load existing prices
            stocks_to_fetch = stored_prices.keys()  # Fetch only stored stocks
            updated_prices = {}

            print("Fetching latest stock prices...")

            for stock in stocks_to_fetch:
                ticker = yf.Ticker(stock)
                history_data = ticker.history(period="1d")

                if not history_data.empty and "Close" in history_data.columns:
                    last_close = history_data["Close"].iloc[-1]
                else:
                    last_close = ticker.info.get("previousClose", 0)

                updated_prices[stock] = round(last_close, 2)

            save_prices(updated_prices)  # Save updated prices
            print("Updated Prices:", updated_prices)

        except Exception as e:
            print("Error fetching stock prices:", e)

        time.sleep(15)  # Fetch every 15 seconds

# **Start Price Fetching Thread**
def start_price_fetch_thread():
    thread = threading.Thread(target=fetch_stock_prices, daemon=True)
    thread.start()

start_price_fetch_thread()

# **API: Frontend Requests Stocks, Backend Returns Cached Prices**
@app.route("/get_prices", methods=["POST"])
def get_prices():
    try:
        data = request.get_json()
        requested_stocks = data.get("stocks", [])  # Get requested stocks
        stored_prices = load_prices()  # Load cached prices

        # **Return only requested stocks**
        response_prices = {stock: stored_prices.get(stock, "Not Available") for stock in requested_stocks}
        return jsonify(response_prices)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
