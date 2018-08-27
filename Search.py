import requests
from flask import Flask, jsonify, current_app
from Settings import ApiUrl

def searchSchedulesByBusNumber(busNumber):
    with current_app.app_context():
        if busNumber is None:
            return Response("The given bus number was None", 422)
        result = requests.get('{}Search/BusSchedules?query={}'.format(ApiUrl, busNumber))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)
        