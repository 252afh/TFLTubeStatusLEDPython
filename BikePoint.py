import requests
from flask import Flask, jsonify, current_app
from Settings import ApiUrl

def getBikePoints():
    with current_app.app_context():
        result = requests.get('{}BikePoint'.format(ApiUrl))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getBikePointById(Id):
    with current_app.app_context():
        if Id is None:
            return Response("No Bike Point Id supplied", 422)
        result = requests.get('{}BikePoint/{}'.format(ApiUrl, Id))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getBikePointByQuery(searchTerm):
    with current_app.app_context():
        if searchTerm is None:
            return Response("No search term supplied", 422)
        result = requests.get('{}BikePoint/Search?query={}'.format(ApiUrl, searchTerm))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)
