import requests
from flask import Flask, jsonify, current_app, Response
from Settings import ApiUrl, appid, appkey

def getPlacesByTypeAndStatus(placeType, activeOnly):
    """ Returns places that match the type
    Required:
        type is the type of place to return
    Optional:
        activeOnly is a boolean whether to include only active places
    Example: BikePoint, true
    Note: The URL given by the TFL documentation does not work
    URL: https://api.tfl.gov.uk/Place/Type/BikePoint?activeOnly=false&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if placeType is None:
            return Response("The given place type was empty", 422)
        resultUrl = '{}Place/Type/{}?{}&{}'.format(ApiUrl, placeType, appid, appkey)
        if activeOnly is not None:
            resultUrl += '&activeOnly={}'.format(activeOnly)
        result = requests.get(resultUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getPlaceById(placeId, includeChildren):
    """ Returns places that match the place id
    Required:
        id is a single string representing the id of a place
    Optional:
    Example: BikePoints_1, true
    Note: The URL given by the TFL documentation does not work
        Another parameter 'includechildren' is always true so has been hard coded in
    URL: https://api.tfl.gov.uk/Place/BikePoints_1?includeChildren=true&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if placeId is None:
            return Response("The given place id was empty", 422)
        resultUrl = '{}Place/{}?{}&{}'.format(ApiUrl, placeId, appid, appkey)
        if includeChildren is not None:
            resultUrl += '&includeChildren={}'.format(includeChildren)
        result = requests.get(resultUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        return jsonify(result.text)

# this does not exist according to TFL, check URL is correct
def getPlacesByBoundingbox(category, includeChildren, placeType, activeOnly, swLat, swLon, neLat, neLon):
    """ Returns a list of places filtered by name
    Required:
        swlat is the southwest latitude for the bounding box
        swlon is the southwest longitude for the bounding box
        nelat is the northeast latitude for the bounding box
        nelon is the northeast latitude for the bounding box 
    Optional:
        type is an array or single string representing the type of place to search for 
        categories is an array or single string representing the categories to include
        includechildren is a boolean whether or not to include children places
        activeonly is a boolean whether to include only active places in the results
    Example: NaptanMetroStation, AccessPoint, true, true, 51.516292, -0.179902, 51.522968, -0.165912
    Note: The URL given by the TFL documentation does not work
        I do not know how exactly categories work so it is always empty for now
    URL: https://api.tfl.gov.uk/Place?includeChildren=true&type=NaptanMetroStation&activeOnly=true&swLat=51.516292&swLon=-0.179902&neLat=51.522968&neLon=-0.165912&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if swLat is None or swLon is None or neLat is None or neLon is None:
            return Response("A given latitude or longitude was empty", 422)
        resultUrl = '{}Place?swLat={}&swLon={}&neLat={}&neLon={}&{}&{}'.format(ApiUrl, swLat, swLon, neLat, neLon, appid, appkey)
        if category is not None:
            resultUrl += '&categories={}'.format(category)
        if includeChildren is not None:
            resultUrl += '&includeChildren={}'.format(includeChildren)
        if placeType is not None:
            resultUrl += '&type={}'.format(placeType)
        if activeOnly is not None:
            resultUrl += '&activeOnly={}'.format(activeOnly)
        result = requests.get(resultUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getPlaceByName(placeName, placeType):
    """ Returns a list of places filtered by name
    Required:
        name is a single string representing the name of a place
    Optional:
        type is an array or single string representing the type of place to search for 
    Example: Brent Cross Stn (LUL), CarPark
    Note: The URL given by the TFL documentation does not work
    URL:  https://api.tfl.gov.uk/Place/Search?name=Brent%20Cross%20Stn%20(LUL)&types=CarPark?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """
    with current_app.app_context():
        if placeName is None or placeType is None:
            return Response("A given value was None", 422)
        result = requests.get('{}Place/Search?name={}&types={}&{}&{}'.format(ApiUrl, placeName, placeType, appid, appkey))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        return jsonify(result.text)