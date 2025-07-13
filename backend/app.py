from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Load rules from JSON file
def load_rules():
    with open(os.path.join(os.path.dirname(__file__), "rules.json"), "r") as f:
        return json.load(f)

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    country = data.get("country", "Norway")  # default to Norway if not provided

    # Load rules for requested country
    rules = load_rules().get(country, [])
    results = []
    for rule in rules:
        # Dummy logic: alternate pass/fail/warning per rule type in config
        results.append({
            "regulation": rule["code"],
            "result": rule["type"].title(),
            "notes": rule["description"]
        })

    return jsonify({
        "status": "success",
        "input": data,
        "results": results
    })

if __name__ == "__main__":
    app.run(debug=True)