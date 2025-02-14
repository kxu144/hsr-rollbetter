import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

from flask import Flask, jsonify, request
from flask_cors import CORS

from enka_api import fetch_player_info
from prob import p
from util import get_asyncio_loop

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app)

executor = ThreadPoolExecutor(max_workers=5)


@app.route('/enka/<uid>', methods=['GET'])
def getData(uid):
    player_info = get_asyncio_loop().run_until_complete(fetch_player_info(uid))
    return jsonify(player_info)

@app.route('/relics', methods=['POST'])
def findProbability():
    start_time = time.time()
    relics = request.get_json()['relics']
    
    results = executor.map(lambda t: p(*t), [(relic, {'CRIT Rate': 1, 'CRIT DMG': 1, 'ATK%': 2/3, 'ATK': 1/4}) for relic in relics])
    output = [{'mainstat': msp, 'substat': ssp, 'combinations': combs} for msp, ssp, combs in results]

    end_time = time.time()
    print(f"/relics Time Elapsed: {end_time - start_time}")
    return jsonify(output)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
