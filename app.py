from flask import Flask, request, jsonify
import yfinance as yf
import threading
import json
import time
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

STOCK_PRICES_FILE = "stock_prices.json"
UPDATE_INTERVAL = 15  # Fetch new prices every 15 seconds

# Load existing stock prices from file (if available)
if os.path.exists(STOCK_PRICES_FILE):
    with open(STOCK_PRICES_FILE, "r") as file:
        stock_prices = json.load(file)
else:
    stock_prices = {}

def get_stock_price(stock):
    """Fetch the latest stock price from Yahoo Finance."""
    try:
        if ".NS" not in stock.upper():
            stock += ".NS"
        ticker = yf.Ticker(stock)
        live_price = ticker.history(period="1d")["Close"].iloc[-1]
        return round(live_price, 2)
    except Exception:
        return None  # Return None if price fetch fails

def update_stock_prices():
    """Background thread to fetch stock prices every 15 sec."""
    global stock_prices
    while True:
        if stock_prices:  # Only fetch for stocks already requested
            for stock in stock_prices.keys():
                price = get_stock_price(stock)
                if price is not None:
                    stock_prices[stock] = price
            
            # Save to JSON file
            with open(STOCK_PRICES_FILE, "w") as file:
                json.dump(stock_prices, file)
        
        time.sleep(UPDATE_INTERVAL)  # Wait before next update

@app.route("/", methods=["GET"])
def home():
    return "Stock Price API is running!"

@app.route("/get_price/<stock>", methods=["GET"])
def get_price(stock):
    """Return latest stock price from cache."""
    global stock_prices
    stock = stock.upper() + ".NS"
    price = stock_prices.get(stock)

    if price is None:
        price = get_stock_price(stock)
        if price is not None:
            stock_prices[stock] = price
            with open(STOCK_PRICES_FILE, "w") as file:
                json.dump(stock_prices, file)
    
    return jsonify({stock: price if price else "Error fetching price"})

@app.route("/get_prices", methods=["POST"])
def get_prices():
    """Return prices for multiple stocks."""
    global stock_prices
    try:
        data = request.get_json()
        stocks = [s.upper() + ".NS" for s in data.get("stocks", [])]
        prices = {}

        for stock in stocks:
            price = stock_prices.get(stock)
            if price is None:
                price = get_stock_price(stock)
                if price is not None:
                    stock_prices[stock] = price
            prices[stock] = price if price else "Error fetching price"

        with open(STOCK_PRICES_FILE, "w") as file:
            json.dump(stock_prices, file)

        return jsonify(prices)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    # Start background price updater
    threading.Thread(target=update_stock_prices, daemon=True).start()
    
    # Start Flask server
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
