import asyncio
from flask import Flask, jsonify
from flask_cors import CORS

from util import fetch_player_info

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app)


@app.route('/enka/<uid>', methods=['GET'])
def getData(uid):
    player_info = asyncio.run(fetch_player_info(uid))
    return jsonify(player_info)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
