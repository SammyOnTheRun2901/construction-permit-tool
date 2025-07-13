from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    return jsonify({
        "status": "success",
        "input": data,
        "result": [
            {"regulation": "TEK17 Section5.2", "result": "Pass", "notes": "Dummy check passed."}
        ]
    })

if __name__ == "__main__":
    app.run(debug=True)