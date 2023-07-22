import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def get_nifty50_open_prices():
    url = "https://www.nseindia.com/market-data/live-equity-market?symbol=NIFTY%2050"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"Error occurred: {err}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    open_prices = {}

    try:
        table = soup.find('table', {'id': 'liveEquityMarket'})
        rows = table.find_all('tr')

        for row in rows[1:]:  # Skip the header row
            cols = row.find_all('td')
            if len(cols) >= 2:
                stock_name = cols[0].text.strip()
                open_price = float(cols[1].text.replace(',', ''))
                open_prices[stock_name] = open_price

    except Exception as e:
        print(f"Error parsing the data: {e}")
        return None

    return open_prices

@app.route('/nifty50/open-prices', methods=['GET'])
def get_nifty50_open_prices_api():
    open_prices = get_nifty50_open_prices()
    if open_prices is None:
        return jsonify({"error": "Failed to fetch NIFTY 50 open prices"}), 500
    return jsonify(open_prices)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
    # app.run(debug=True)
