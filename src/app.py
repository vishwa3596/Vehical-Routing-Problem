from flask import Flask, jsonify
from main import OptimalPath
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    sm = OptimalPath()
    greedy_prop = jsonify(sm.greedy_sol())
    inter_prop = jsonify(sm.InterLocalSearch())
    intra_prop = jsonify(sm.IntraLocalSearch())
    return intra_prop

if __name__ == "__main__":
    app.run(port=8000)
    app.debug(True)
