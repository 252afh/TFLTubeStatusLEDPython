import requests
from flask import Flask, jsonify, current_app, Response
from Settings import ApiUrl

def getBikePoints():
    with current_app.app_context():
        result = requests.get('{}BikePoint'.format(ApiUrl))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getBikePointById(Id):
    with current_app.app_context():
        if Id is None:
            return Response("No Bike Point Id supplied", 422)
        result = requests.get('{}BikePoint/{}'.format(ApiUrl, Id))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getBikePointByQuery(searchTerm):
    with current_app.app_context():
        if searchTerm is None:
            return Response("No search term supplied", 422)
        result = requests.get('{}BikePoint/Search?query={}'.format(ApiUrl, searchTerm))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)
