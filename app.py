from flask import Flask, jsonify

from nsepython import *

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the NSE Market Data API! Use /get-data to fetch market data."

@app.route('/get-data')
def get_data():
    # Fetch market data
    fii_dii = fii_dii_cash()
    nifty_price = nse_eq("NIFTY 50")['lastPrice']
    sensex_price = nse_eq("SENSEX")['lastPrice']
    banknifty_price = nse_eq("BANKNIFTY")['lastPrice']
    option_chain = nse_optionchain_scrapper("BANKNIFTY")  

    data = {
        "FII_DII": fii_dii,
        "Nifty50": nifty_price,
        "Sensex": sensex_price,
        "BankNifty": banknifty_price,
        "OptionChain": option_chain
    }

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
