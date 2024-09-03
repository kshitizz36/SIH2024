from flask import Flask, jsonify, request
from src import algorithm
app = Flask(__name__)


@app.route('/map', methods=['POST'])
def get_user_input():
    user_input = request.json 
    print("Received user input:", user_input) 

    x = algorithm.main(user_input['start'],user_input['end'])

    
    result = {
    "path": x[0],
    "eta": x[1][2],
    "km": x[3],
    "fuel": x[-3],
    }
    print('sendin')

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)