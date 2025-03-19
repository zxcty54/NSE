from flask import Flask, request, jsonify
import yfinance as yf
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def get_stock_price(stock):
    """Fetch the latest closing price of a stock, handling missing data."""
    try:
        if ".NS" not in stock.upper():
            stock += ".NS"
        ticker = yf.Ticker(stock)
        history_data = ticker.history(period="1d")

        # Check if data is empty or missing
        if history_data.empty or "Close" not in history_data.columns:
            live_price = ticker.info.get("previousClose", 0)  # Use last known close as backup
        else:
            live_price = history_data["Close"].iloc[-1]

        return round(live_price, 2)
    except Exception as e:
        return str(e)

@app.route("/get_price/<stock>", methods=["GET"])
def get_price(stock):
    """API to get the latest price of a single stock."""
    price = get_stock_price(stock)
    if isinstance(price, str):  # If error occurred
        return jsonify({"error": price})
    return jsonify({stock: price})

@app.route("/get_prices", methods=["POST"])
def get_prices():
    """API to get the latest prices of multiple stocks."""
    try:
        data = request.get_json()
        stocks = data.get("stocks", [])
        prices = {stock: get_stock_price(stock) for stock in stocks}
        return jsonify(prices)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
