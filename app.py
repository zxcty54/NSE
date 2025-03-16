from flask import Flask, jsonify
from nsetools import Nse

app = Flask(__name__)
nse = Nse()

@app.route('/get-data')
def get_data():
    try:
        # Fetching FII/DII data (nsetools doesn't provide this directly)
        fii_dii_data = "FII/DII data is not available in nsetools"

        # Fetching index prices
        nifty_data = nse.get_index_quote("nifty 50")
        sensex_data = nse.get_index_quote("s&p bse sensex")
        banknifty_data = nse.get_index_quote("nifty bank")

        # Extract prices safely
        nifty_price = nifty_data.get("lastPrice", "Data Not Available")
        sensex_price = sensex_data.get("lastPrice", "Data Not Available")
        banknifty_price = banknifty_data.get("lastPrice", "Data Not Available")

        # Prepare JSON response
        data = {
            "FII_DII": fii_dii_data,
            "Nifty50": nifty_price,
            "Sensex": sensex_price,
            "BankNifty": banknifty_price
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
