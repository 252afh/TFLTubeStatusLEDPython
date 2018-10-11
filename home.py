from flask import Flask, jsonify, json, request, Response
from flask_sslify import SSLify
import sys
sys.path.append('/home/pi/Documents/FlaskAPI/TFLAPIScripts')
from Line import *
from test import *
app = Flask(__name__)
sslify = SSLify(app)

@app.route('/')
def checkStatus():
    return 'Hello, World!'

@app.route('/Line/getAllLineStatus', methods=['GET'])
def getAllLineStatus():
    result = getLineStatus()
    return result

@app.route('/Line/getLinesById', methods=['GET'])
def getLinesById():
    Id = request.args.get('id', default=None, type=str)
    if type(Id) is not str:
        return Response("The given Id was not a string", 422)
    result = getLineById(Id)
    return result

@app.route('/Line/getByMode', methods=['GET'])
def getLineByMode():
    mode = request.args.get('mode', default = None, type = str)
    if type(mode) is not str:
        return Response("The given mode was not a string", 422)
    result = getLinesByMode(mode)
    return result

@app.route('/Line/getByModeAndId', methods=['GET'])
def getLineByModeAndId():
    mode = request.args.get('mode',default=None,type=str)
    id = request.args.get('mode',default=None,type=str)
    if type(id) is not str or type(mode) is not str:
        return Response("The given mode or id was not a string", 422)
    result = getLineByIdAndMode(id, mode)
    return result

@app.route('/Line/getLineInfoByDateId',methods=['GET'])
def getLineByDateAndId():
    