from flask import Flask, request, jsonify
from flask_cors import CORS  
import json
app = Flask(__name__)
CORS(app) 

@app.route("/recibir", methods=["POST"])
def recibir():
    data = request.get_json()

    pretty_json = json.dumps(data, indent=4)

    print(pretty_json)

    return jsonify(json.loads(pretty_json))

app.run(host="0.0.0.0", port=8081)