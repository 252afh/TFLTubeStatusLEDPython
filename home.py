from flask import Flask, jsonify, json, request, Response
from flask_sslify import SSLify
import sys
sys.path.append('/home/pi/Documents/FlaskAPI/TFLAPIScripts')
#from Line import *
from test import *
app = Flask(__name__)
sslify = SSLify(app)

@app.route('/')
def checkStatus():
    return 'Hello, World!'

@app.route('/Line/getByMode', methods=['GET'])
def getLineByMode():
    mode = request.args.get('mode', default = None, type = str)
    if mode is None:
        return ("The given mode was None", 400)
    result = getLinesByMode(mode)
    if result is None:
        return ("The requested result was None", 400)
    return result