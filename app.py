import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, jsonify

app = Flask(__name__)

# File to store FII/DII data
DATA_FILE = "fii_dii_data.json"

# NSE FII/DII Data URL
URL = "https://www.nseindia.com/reports/foreign-institutional-investors-report"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.nseindia.com"
}

def fetch_fii_dii_data():
    """Fetch FII/DII data from NSE and save to JSON file."""
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        response = session.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")
        data_table = soup.find("table")  # Find table with FII/DII data
        
        if data_table:
            rows = data_table.find_all("tr")[1:]  # Skip header row
            fii_dii_list = []
            for row in rows:
                cols = row.find_all("td")
                fii_dii_list.append({
                    "Date": cols[0].text.strip(),
                    "FII_Buy": cols[1].text.strip(),
                    "FII_Sell": cols[2].text.strip(),
                    "DII_Buy": cols[3].text.strip(),
                    "DII_Sell": cols[4].text.strip(),
                    "Net_FII": cols[5].text.strip(),
                    "Net_DII": cols[6].text.strip()
                })
            
            # Save data to JSON file
            with open(DATA_FILE, "w") as f:
                json.dump(fii_dii_list, f, indent=4)

            return fii_dii_list
        else:
            return {"error": "No data found."}
    
    except Exception as e:
        return {"error": str(e)}

@app.route("/fii-dii")
def get_fii_dii():
    """Serve FII/DII data from JSON file."""
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Data not available. Run fetch_fii_dii_data() first."})

if __name__ == "__main__":
    # Fetch data once per day manually or via a cron job
    fetch_fii_dii_data()
    app.run(debug=True, host="0.0.0.0", port=5000)
