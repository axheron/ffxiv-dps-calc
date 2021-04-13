"""ffxiv-dps-calc – dps calculations for the smart masses"""

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

if __name__ == "__main__":
    app.run()

import xivdpscalc.routing
