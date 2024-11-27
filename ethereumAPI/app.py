import logging
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ETH_STAKING_APR = 0.05  # Annual percentage rate for staking (5%)

def get_eth_price():
    try:
        response = requests.get('https://api.coinpaprika.com/v1/tickers/eth-ethereum')
        response.raise_for_status()
        data = response.json()
        return data['quotes']['USD']['price']
    except Exception as e:
        logging.error(f"Error fetching ETH price: {e}")
        return None

@app.route('/stake-roi', methods=['POST'])
def calculate_roi():
    data = request.json
    eth_amount = data.get('eth_amount', None)
    if eth_amount is None or not isinstance(eth_amount, (int, float)):
        return jsonify({"error": "Invalid input. Provide a numeric eth_amount."}), 400

    eth_price = get_eth_price()
    if eth_price is None:
        return jsonify({"error": "Failed to fetch ETH price"}), 500

    annual_roi = eth_amount * eth_price * ETH_STAKING_APR
    monthly_roi = annual_roi / 12

    return jsonify({
        "eth_amount": eth_amount,
        "eth_price_usd": round(eth_price, 2),
        "expected_monthly_roi_usd": round(monthly_roi, 2)
    })
