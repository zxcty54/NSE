import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf

@app.route("/get_price/<stock>", methods=["GET", "POST"])
def get_price(stock=None):
    if request.method == "POST":
        data = request.json
        stock = data.get("stock")

    if not stock:
        return jsonify({"error": "Stock symbol required"}), 400

    try:
        ticker = yf.Ticker(stock)
        current_price = ticker.history(period="1d")["Close"].iloc[-1]
        return jsonify({"stock": stock, "current_price": round(current_price, 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
