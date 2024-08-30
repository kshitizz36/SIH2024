from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/map', methods=['POST'])
def get_user_input():
    user_input = request.json 
    print("Received user input:", user_input) 

    result = {
    "path": [
        [12.34, 56.78],
        [13.34, 57.78],
        [14.34, 58.78]
    ],
    "eta": 5.5,
    "km": 120.0,
    "fuel": 30.0
}


    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)