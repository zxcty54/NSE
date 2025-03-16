from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route("/get_price", methods=["POST"])
def get_price():
    data = request.json
    stock = data["stock"]
    
    try:
        ticker = yf.Ticker(stock)
        current_price = ticker.history(period="1d")["Close"].iloc[-1]  # Fetch latest price
        return jsonify({"stock": stock, "current_price": round(current_price, 2)})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
