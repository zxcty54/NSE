from flask import Flask, jsonify
from jugaad_data.nse import get_fii_dii_data

app = Flask(__name__)

@app.route('/fii-dii', methods=['GET'])
def fii_dii():
    try:
        data = get_fii_dii_data(days=10)  # Fetch last 10 days' data
        return jsonify(data.to_dict(orient="records"))  # Convert DataFrame to JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
