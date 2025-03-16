from flask import Flask, request, jsonify
import yfinance as yf
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  

@app.route("/get_price/<stock>", methods=["GET"])
def get_price(stock):
    try:
        if ".NS" not in stock.upper():
            stock += ".NS"  # Auto-append .NS if missing
        ticker = yf.Ticker(stock)
        live_price = ticker.history(period="1d")["Close"].iloc[-1]
        return jsonify({stock: round(live_price, 2)})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/get_prices", methods=["POST"])
def get_prices():
    try:
        data = request.get_json()
        stocks = data.get("stocks", [])
        prices = {}

        for stock in stocks:
            if ".NS" not in stock.upper():
                stock += ".NS"  # Auto-append .NS if missing
            ticker = yf.Ticker(stock)
            live_price = ticker.history(period="1d")["Close"].iloc[-1]
            prices[stock] = round(live_price, 2)

        return jsonify(prices)
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
