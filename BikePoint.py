import requests
from flask import Flask, jsonify, current_app, Response
from Settings import ApiUrl, appid, appkey

def getBikePoints():
    """ Returns information about all bike points
    Required:
    Optional:
    Example:
    Note: The URL given by the TFL documentation does not work
    URL: https://api.tfl.gov.uk/BikePoint?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        result = requests.get('{}BikePoint?{}&{}'.format(ApiUrl, appid, appkey))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getBikePointById(Id):
    """ Returns information about a bike point based on the id
    Required:
        id is a single string representing the bikepoints id
    Optional:
    Example: BikePoints_1
    Note: The URL given by the TFL documentation does not work
    URL: https://api.tfl.gov.uk/BikePoint/BikePoints_1?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if Id is None:
            return Response("No Bike Point Id supplied", 422)
        result = requests.get('{}BikePoint/{}?{}&{}'.format(ApiUrl, Id, appid, appkey))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getBikePointByQuery(searchTerm):
    """ Returns information about a bike point based on the search query
    Required:
        query is a single string representing the search term
    Optional:
    Example: St. James
    Note: The URL given by the TFL documentation does not work
    URL: https://api.tfl.gov.uk/BikePoint/Search?query=St.%20James&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if searchTerm is None:
            return Response("No search term supplied", 422)
        result = requests.get('{}BikePoint/Search?query={}&{}&{}'.format(ApiUrl, searchTerm, appid, appkey))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)
