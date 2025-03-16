from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

def get_fii_dii_data():
    url = "https://www.nseindia.com/api/fiidiiTradeReact"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/"
    }
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=10)
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def home():
    fii_dii_data = get_fii_dii_data()
    return jsonify(fii_dii_data)

if __name__ == "__main__":
    app.run(debug=True)
