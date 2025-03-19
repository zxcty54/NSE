from flask import Flask, request, jsonify
import yfinance as yf
from flask_cors import CORS
import os
import json
import threading
import time

app = Flask(__name__)
CORS(app)

# Global variable to store stock prices
stock_prices = {}

# Function to fetch stock price
def get_stock_price(stock):
    """Fetch latest stock price from Yahoo Finance."""
    try:
        if not stock.upper().endswith(".NS"):
            stock += ".NS"

        ticker = yf.Ticker(stock)
        history_data = ticker.history(period="1d")

        if history_data.empty:
            return ticker.info.get("previousClose", 0)  # Use previous close if no data
        
        return round(history_data["Close"].iloc[-1], 2)
    except Exception as e:
        return str(e)

# Background thread to update stock prices every 30 minutes
def update_stock_prices():
    global stock_prices
    while True:
        try:
            if stock_prices:  # Fetch only for stored stocks
                for stock in stock_prices.keys():
                    stock_prices[stock] = get_stock_price(stock)
                with open("prices.json", "w") as f:
                    json.dump(stock_prices, f)
        except Exception as e:
            print("Error updating stock prices:", str(e))
        time.sleep(1800)  # Update every 30 minutes

# API to get stock price (from cache)
@app.route("/get_price/<stock>", methods=["GET"])
def get_price(stock):
    global stock_prices
    if stock in stock_prices:
        return jsonify({stock: stock_prices[stock]})
    else:
        price = get_stock_price(stock)
        stock_prices[stock] = price
        return jsonify({stock: price})

# API to get multiple stock prices
@app.route("/get_prices", methods=["POST"])
def get_prices():
    try:
        data = request.get_json()
        stocks = data.get("stocks", [])
        prices = {}

        for stock in stocks:
            if stock in stock_prices:
                prices[stock] = stock_prices[stock]
            else:
                prices[stock] = get_stock_price(stock)
                stock_prices[stock] = prices[stock]

        return jsonify(prices)
    except Exception as e:
        return jsonify({"error": str(e)})

# Start background thread
thread = threading.Thread(target=update_stock_prices, daemon=True)
thread.start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
