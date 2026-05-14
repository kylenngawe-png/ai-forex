from flask import Flask, jsonify
from flask_cors import CORS
import MetaTrader5 as mt5

app = Flask(__name__)
CORS(app)

# CONNECT TO MT5 TERMINAL
mt5.initialize()

@app.route("/account")
def account():
    info = mt5.account_info()

    return jsonify({
        "balance": info.balance,
        "equity": info.equity,
        "profit": info.profit,
        "currency": info.currency
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
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 50)

    closes = [r[4] for r in rates]

    ema_fast = sum(closes[-10:]) / 10
    ema_slow = sum(closes[-20:]) / 20

    if ema_fast > ema_slow:
        signal = "BUY"
    else:
        signal = "SELL"

    return jsonify({
        "signal": signal,
        "entry": closes[-1],
        "confidence": 75
    })

if __name__ == "__main__":
    app.run(debug=True)
