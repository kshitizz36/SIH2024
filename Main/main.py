from flask import Flask, jsonify, request
from flask_cors import CORS
from src import algorithm
app = Flask(__name__)
CORS(app)

@app.route('/map', methods=['POST'])
def get_user_input():
    user_input = request.json 
    print("Received user input:\n\n", user_input,"\n\n\n") 

    x = algorithm.main(user_input['start'],user_input['end'],float(user_input['ship']['Speed']))

    
    result = {
    "path": x[0],
    "eta": x[1],
    "km": x[2],
    "fuel": x[3],
    }


    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)