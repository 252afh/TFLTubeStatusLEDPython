import requests
from flask import Flask, jsonify, current_app, Response, request
from Settings import ApiUrl, appid, appkey
from DatabaseAccess import InsertError

def getCarParkOccupancyById(carParkId):
    """ Returns occupancy of a carpark based on the id
    Required:
        id is a single string for the car park id to search for
    Optional:
    Example: CarParks_800477
    Note: The URL given by the TFL documentation does not work
    URL: https://api.tfl.gov.uk/Occupancy/CarPark/CarParks_800491?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if carParkId is None:
            InsertError('carParkId must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("The given carpark id was empty", 422)
        result = requests.get('{}Occupancy/CarPark/{}?{}&{}'.format(ApiUrl, carParkId, appid, appkey))
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getChargeConnectorById(connectorId):
    """ Returns occupancy of a charge point based on the id
    Required:
        id is an array or single string for the charge point id to search for
    Optional:
    Example: ChargePointESB-UT092S-1
    Note: The URL given by the TFL documentation does not work
    URL: https://api.tfl.gov.uk/Occupancy/ChargeConnector/ChargePointESB-UT092S-1?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if connectorId is None:
            InsertError('connectorId must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("The given charge connector id was empty", 422)
        result = requests.get('{}Occupancy/ChargeConnector/{}?{}&{}'.format(ApiUrl, connectorId, appid, appkey))
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getBikePointOccupancyById(bikePointId):
    """ Returns occupancy of a bikepoint based on the id
    Required:
        id is the bikepoint id to search for
    Optional:
    Example: BikePoints_1
    Note: The URL given by the TFL documentation does not work
    URL:https://api.tfl.gov.uk/Occupancy/BikePoints/BikePoints_1?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if bikePointId is None:
            InsertError('bikePointId must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("The given bike point id is empty", 422)
        result = requests.get('{}Occupancy/BikePoints/{}?{}&{}'.format(ApiUrl, bikePointId, appid, appkey))
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)