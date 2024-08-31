from flask import Flask, jsonify, request
from src import algorithm
app = Flask(__name__)


@app.route('/map', methods=['POST'])
def get_user_input():
    user_input = request.json 
    print("Received user input:", user_input) 

    x = algorithm.main()

    
    result = {
    "path": x,
    "eta": 5.5,
    "km": 120.0,
    "fuel": 30.0
}


    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)