import asyncio
from flask import Flask, jsonify, request
from flask_cors import CORS

from prob import p
from util import fetch_player_info

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app)


@app.route('/enka/<uid>', methods=['GET'])
def getData(uid):
    player_info = asyncio.run(fetch_player_info(uid))
    return jsonify(player_info)

@app.route('/relic', methods=['POST'])
def findProbability():
    relic = request.get_json()
    msp, ssp, combs = p(relic, {'CRIT Rate': 1, 'CRIT DMG': 1, 'ATK%': 2/3, 'ATK': 1/4})

    return jsonify({'mainstat': msp, 'substat': ssp, 'combinations': combs})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
