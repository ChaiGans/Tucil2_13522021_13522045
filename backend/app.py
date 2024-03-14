from flask import Flask, request, jsonify
from main import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/dnc', methods=['POST'])
def dnc_beizer_curve():
    try :
        if (request.method == 'POST'):
            data = request.json
            bezier_curve_points = generate_bezier_dnc(data['start_point'], data['control_points'], data['end_point'], data['iterations'])
            return jsonify(bezier_curve_points)
    except:
        return jsonify({"message" : "error caught ini dnc_beizer_curve"})

@app.route('/bruteforce', methods=['POST'])
def bruteforce_beizer_curve():
    try :
        if (request.method == 'POST'):
            data = request.json
            bezier_curve_points = generate_bezier_bruteforce(data['start_point'], data['control_points'], data['end_point'], data['iterations'])
            return jsonify(bezier_curve_points)
    except:
        return jsonify({"message" : "error caught ini dnc_beizer_curve"})
