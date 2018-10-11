import requests
from flask import Flask, jsonify, current_app, Response
from Settings import ApiUrl

def getPlacesByTypeAndStatus(placeType, activeOnly):
    with current_app.app_context():
        if placeType is None:
            return Response("The given place type was empty", 422)
        resultUrl = '{}Place/Type/{}'.format(ApiUrl, placeType)
        if activeOnly is not None:
            resultUrl += '?activeOnly={}'.format(activeOnly)
        result = requests.get(resultUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the result")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getPlaceById(placeId, includeChildren):
    with current_app.app_context():
        if placeId is None:
            return Response("The given place id was empty", 422)
        resultUrl = '{}Place/{}'.format(ApiUrl, placeId)
        if includeChildren is not None:
            resultUrl += '?includeChildren={}'.format(includeChildren)
        result = requests.get(resultUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

# this does not exist according to TFL, check URL is correct
def getPlacesByBoundingbox(category, includeChildren, placeType, activeOnly, swLat, swLon, neLat, neLon):
    with current_app.app_context():
        if swLat is None or swLon is None or neLat is None or neLon is None:
            return Response("A given latitude or longitude was empty", 422)
        resultUrl = '{}Place?bbBoxpoints.swLat={}&bbBoxpoints.swLon={}&bbBoxpoints.neLat={}&bbBoxpoints.neLon={}'.format(ApiUrl, swLat, swLon, neLat, neLon)
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
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

# same problem as above, does not exist
def getPlaceAtLongAndLat(placeType, lat, lng, locLat, locLong):
    with current_app.app_context():
        if placeType is None or lat is None or lng is None or locLat is None or locLong is None:
            return Response("A given value was None", 422)
        result = requests.get('{}Place/{}/At/{{Lat}}/{{Lon}}?lat={}&lon={}&location.lat={}&location.lon={}'.format(ApiUrl, placeType, lat, lng, locLat, locLong))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getPlaceByBoudingBox(zoom, placeType, width, height, lat, lon, locLat, locLon):
    with current_app.app_context():
        if zoom is None:
            zoom = 1
        if placeType is None or width is None or height is None or lat is None or lon is None or locLat is None or locLon is None:
            return Response("A given value was None", 422)
        result = requests.get('{}Place/{}/overlay/{}/{{Lat}}/{{Lon}}/{}/{}?lat={}&lon={}&location.lat={}&location.lon={}'.format(ApiUrl, placeType, zoom, lat, locLat, lat, lon, locLat, locLon))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)

def getPlaceByName(placeName, placeType):
    with current_app.app_context():
        if placeName is None or placeType is None:
            return Response("A given value was None", 422)
        result = requests.get('{}Place/Search?name={}&types={}'.format(ApiUrl, placeName, placeType))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        if result.text[0] is '[':
            print("Trimming the '[]' characters from the JSON response")
            result.text = result.text[1:-1]
        return jsonify(result.text)