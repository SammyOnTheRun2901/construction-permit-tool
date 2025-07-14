from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

def load_rules():
    with open(os.path.join(os.path.dirname(__file__), "rules.json"), "r") as f:
        return json.load(f)

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    country = data.get("country", "Norway")
    rules = load_rules().get(country, [])
    results = []

    for rule in rules:
        field = rule.get("field")
        value = data.get(field)
        result = "Warning"
        notes = rule["description"]

        # Numeric checks
        if value is not None:
            try:
                val = float(value)
            except (ValueError, TypeError):
                val = value  # keep as is if not a number

            if "min" in rule and "max" in rule:
                if val < rule["min"]:
                    result = "Fail"
                    notes += f" Value ({val}) is less than minimum allowed ({rule['min']})."
                elif val > rule["max"]:
                    result = "Fail"
                    notes += f" Value ({val}) exceeds maximum allowed ({rule['max']})."
                else:
                    result = "Pass"
            elif "min" in rule:
                if val < rule["min"]:
                    result = "Fail"
                    notes += f" Value ({val}) is less than minimum required ({rule['min']})."
                else:
                    result = "Pass"
            elif "max" in rule:
                if val > rule["max"]:
                    result = "Fail"
                    notes += f" Value ({val}) exceeds maximum allowed ({rule['max']})."
                else:
                    result = "Pass"
            elif "required" in rule:
                if val:
                    result = "Pass"
                else:
                    result = "Fail"
                    notes += " Required but not provided."
            else:
                result = "Pass"

        # Boolean checks
        elif "required" in rule:
            if value:
                result = "Pass"
            else:
                result = "Fail"
                notes += " Required but not provided."

        else:
            result = "Warning"
            notes += " No value provided for check."

        results.append({
            "regulation": rule["code"],
            "result": result,
            "notes": notes
        })

    return jsonify({
        "status": "success",
        "input": data,
        "results": results
    })

if __name__ == "__main__":
    app.run(debug=True)