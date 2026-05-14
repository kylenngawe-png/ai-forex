from flask import Flask, jsonify
from flask_cors import CORS
import MetaTrader5 as mt5

app = Flask(__name__)
CORS(app)

# initialize MT5
mt5.initialize()

@app.route("/account")
def account():
    info = mt5.account_info()
    return jsonify({
        "balance": float(info.balance),
        "equity": float(info.equity),
        "profit": float(info.profit)
    })

@app.route("/price/<symbol>")
def price(symbol):
    tick = mt5.symbol_info_tick(symbol)

    return jsonify({
        "symbol": symbol,
        "bid": tick.bid,
        "ask": tick.ask
    })

@app.route("/signal/<symbol>")
def signal(symbol):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 100)

    closes = [r[4] for r in rates]

    # REAL SIMPLE STRATEGY (EMA LOGIC)
    fast = sum(closes[-10:]) / 10
    slow = sum(closes[-30:]) / 30

    if fast > slow:
        sig = "BUY"
    else:
        sig = "SELL"

    entry = closes[-1]

    return jsonify({
        "signal": sig,
        "entry": entry,
        "confidence": 70
    })

if __name__ == "__main__":
    app.run(debug=True)
