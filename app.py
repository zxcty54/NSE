from flask import Flask, jsonify
from nsetools import Nse
import requests

app = Flask(__name__)
nse = Nse()

def get_fii_dii_data():
    url = "https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES_IN_F&O"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}

@app.route('/get-data')
def get_data():
    fii_dii = get_fii_dii_data()  # Fetch FII/DII data
    nifty_price = nse.get_index_quote("nifty 50")['lastPrice']
    sensex_price = nse.get_index_quote("sensex")['lastPrice']
    banknifty_price = nse.get_index_quote("nifty bank")['lastPrice']

    data = {
        "FII_DII": fii_dii,
        "Nifty50": nifty_price,
        "Sensex": sensex_price,
        "BankNifty": banknifty_price
    }

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
