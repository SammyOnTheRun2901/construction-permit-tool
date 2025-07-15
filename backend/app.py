from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import traceback
import json  # <--- missing import

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

# Set your Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
print(genai.list_models())
 
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

@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.get_json()
    form_data = data.get('form_data')
    prompt = (
        "You are an expert in building regulations for Norway and Denmark. "
        "Review the following construction permit application and give concise suggestions for improvements or flag issues:\n"
        f"{form_data}"
    )
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        # The response format may change; check the API docs for details
        suggestion = response.text if hasattr(response, "text") else str(response)
        return jsonify({"suggestion": suggestion})
    except Exception as e:  # <-- Fixed indentation here
        print("An exception occurred!")  # Step 7: Exception caught
        print("Error:", repr(e))
        traceback.print_exc()  # Step 8: Print full traceback for details
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)