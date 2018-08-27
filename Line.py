import requests
from flask import Flask, jsonify, current_app
from Settings import ApiUrl

def getLineStatus():
    with current_app.app_context():
        result = requests.get('{}Line/Mode/tube%2Cdlr/Status'.format(ApiUrl))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getLineById(Id):
    with current_app.app_context():
        if Id is None:
            return Response("The supplied Id is empty", 422)
        result = requests.get('{}Line/{}'.format(ApiUrl, Id))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getLinesByMode(mode):
    with current_app.app_context():
        if mode is None:
            return Response("The supplied mode is empty", 422)
        result = requests.get('{}Line/Mode/{}'.format(ApiUrl, mode))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getLineByIdAndMode(Id, mode):
    with current_app.app_context():
        if Id is None:
            return Response("The supplied Id was empty", 422)
        requestUrl = '{}Line/{}/Route'.format(ApiUrl, Id)
        if mode is not None:
            requestUrl += '?serviceTypes={}'.format(mode)
        result = requests.get(requestUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getLineInfoByDateAndId(Id, startDate, endDate, detail):
    with current_app.app_context():
        if id is None:
            return Response("The supplied Id was empty", 422)
        if startDate is None:
            return Response("The supplied start date was empty", 422)
        if endDate is None:
            return Response("The supplied end date was empty", 422)
        requestUrl = '{}Line/{}/Status/{}/to/{}'.format(ApiUrl, Id, startDate, endDate)
        if detail is not None:
            requestUrl += '?detail={}'.format(detail)
        result = requests.get(requestUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getLineStatusbyId(Id, detail):
    with current_app.app_context():
        if Id is None:
            return Response("The supplied Id was empty", 422)
        requestUrl = '{}Line/{}/Status'.format(ApiUrl, Id)
        if detail is not None:
            requestUrl += '?detail={}'.format(detail)
        result = requests.get(requestUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getLinesBySeverityCode(severitycode):
    with current_app.app_context():
        if severitycode is None:
            return Response("The supplied severity was empty", 422)
        result = requests.get('{}Line/Status/{}'.format(ApiUrl, severitycode))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getLineStatusByMode(mode, detail):
    with current_app.app_context():
        if mode is None:
            return Response("The supplied line was empty", 422)
        requestUrl = '{}Line/Mode/{mode}/Status'.format(ApiUrl, mode)
        if detail is not None:
            requestUrl += '?detail={}'.format(detail)
        result = requests.get(requestUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getStationsOnLine(Id, tflOnly):
    with current_app.app_context():
        if Id is None:
            return Response("The supplied Id was empty", 422)
        requestUrl = '{}Line/{}/StopPoints'.format(ApiUrl, Id)
        if tflOnly is not None:
            requestUrl += '?tflOperatedNationalRailStationsOnly={}'.format(tflOnly)
        result = requests.get(requestUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getTimetableForStationOnLine(stationId, lineId):
    with current_app.app_context():
        if stationId is None:
            return Response("The given station id was empty", 422)
        if lineId is None:
            return Response("The given line id is empty", 422)
        result = requests.get('{}Line/{}/Timetable/{}'.format(ApiUrl, lineId, stationId))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getTimetableForJourney(sourceId, destId, lineId):
    with current_app.app_context():
        if sourceId is None:
            return Response("The given source station id is empty", 422)
        if destId is None:
            return Response("The given destination station id is empty", 422)
        if lineId is None:
            return Response("The given line id is empty", 422)
        result = requests.get('{}Line/{}/Timetable/{}/to/{}'.format(ApiUrl, lineId, sourceId, destId))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getDisruptionsForGivenLine(lineId):
    with current_app.app_context():
        if lineId is None:
            return Response("The given line id was empty", 422)
        result = requests.get('{}Line/{}/Disruption'.format(ApiUrl, lineId))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getDisruptionsForGivenMode(modeId):
    with current_app.app_context():
        if modeId is None:
            return Response("The given line mode was empty", 422)
        result = requests.get('{}Line/Mode/{}/Disruption'.format(ApiUrl, modeId))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getArrivalsForLineAndStop(lineId, sourceId, destId, direction):
    with current_app.app_context():
        if lineId is None:
            return Response("The given line id was empty", 422)
        if sourceId is None:
            return Response("The given line id was empty", 422)
        resultUrl = '{}Line/{}/Arrivals/'.format(ApiUrl, lineId, sourceId, direction, destId)
        if sourceId is not None:
            resultUrl += '{}'.format(sourceId)
        if direction is not None:
            resultUrl += '?direction={}'.format(direction)
        if destId is not None:
            resultUrl += '&destinationStationId={}'.format(destId)
        result = requests.get(resultUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)