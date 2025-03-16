from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route("/get_price/<stock>", methods=["GET"])
def get_price(stock):
    try:
        ticker = yf.Ticker(stock)
        live_price = ticker.history(period="1d")["Close"].iloc[-1]
        return jsonify({stock: round(live_price, 2)})
    except Exception as e:
        return jsonify({"error": str(e)})

# ✅ New Endpoint to Fetch Multiple Stock Prices
@app.route("/get_prices", methods=["POST"])
def get_prices():
    try:
        data = request.get_json()
        stocks = data.get("stocks", [])  # List of stock symbols
        prices = {}

        for stock in stocks:
            ticker = yf.Ticker(stock)
            live_price = ticker.history(period="1d")["Close"].iloc[-1]
            prices[stock] = round(live_price, 2)

        return jsonify(prices)
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
