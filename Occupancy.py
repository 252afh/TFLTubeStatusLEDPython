import requests
from flask import Flask, jsonify, current_app, Response
from Settings import ApiUrl

def getCarParkOccupancyById(carParkId):
    with current_app.app_context():
        if carParkId is None:
            return Response("The given carpark id was empty", 422)
        result = requests.get('{}Occupancy/CarPark/{}'.format(ApiUrl, carParkId))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getChargeConnectorById(connectorId):
    with current_app.app_context():
        if connectorId is None:
            return Response("The given charge connector id was empty", 422)
        result = requests.get('{}Occupancy/ChargeConnector/{}'.format(ApiUrl, connectorId))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getBikePointOccupancyById(bikePointId):
    with current_app.app_context():
        if bikePointId is None:
            return Response("The given bike point id is empty", 422)
        result = requests.get('{}Occupancy/BikePoints/{}'.format(ApiUrl, bikePointId))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)