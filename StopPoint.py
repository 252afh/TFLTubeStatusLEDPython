import requests
from flask import Flask, jsonify, current_app, Response
from Settings import ApiUrl

def getStopPointById (stopId, isCrowded):
    if stopId is None:
        return Response("The given stop id was None", 422)
    resultUrl = '{}StopPoint/{}'.format(ApiUrl, stopId)
    if isCrowded is not None:
        resultUrl += '?includeCrowdingData={}'.format(isCrowded)
    result = requests.get(resultUrl)
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)

def getStopPointByIdAndType (stopId, placeType):
    if stopId is None or placeType is None:
        return Response("The given arguments are None", 422)
    result = requests.get('{}StopPoint/{}/placeTypes?placeTypes={}'.format(ApiUrl, stopId, placeType))
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)

def getCrowdingByIdAndLineAndDirection (stopId, lineId, direction):
    if stopId is None or lineId is None or direction is None:
        return Response("The given arguments are None", 422)
    result = requests.get('{}StopPoint/{}/Crowding/{}?direction={}'.format(ApiUrl, stopId, lineId, direction))
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)

def getStopsOfType (stopType):
    if stopType is None:
        return Response("The given argument was None", 422)
    result = requests.get('{}StopPoint/Type/{}'.format(ApiUrl, stopType))
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)

def getStopOfTypeWithPage (stopType, pageNumber):
    if stopType is None or pageNumber is None or type(pageNumber) is not int:
        return Response("The given arguments are None or the wrong type", 422)
    result = requests.get('{}StopPoint/Type/{}/page/{}'.format(ApiUrl, stopType, pageNumber))
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)

def getServicesForStop (stopId, lineId, serviceMode):
    if stopId is None:
        return Response("The given stop id is None", 422)
    resultUrl = '{}StopPoint/ServiceTypes?id={}'.format(ApiUrl, stopId)
    if lineId is not None:
        resultUrl += '&lineIds={}'.format(lineId)
    if serviceMode is not None:
        resultUrl += '&modes={}'.format(serviceMode)
    result = requests.get(resultUrl)
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)

def getArrivalsByStopId (stopId):
    if stopId is None:
        return Response("The given stop id is None", 422)
    result = requests.get('{}StopPoint/{}/Arrivals'.format(ApiUrl, stopId))
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)

def getStopsFromStationAndLine (stopId, lineId, service):
    if stopId is None or lineId is None:
        return Response("The given stop or line id was None", 422)
    resultUrl = '{}StopPoint/{}/CanReachOnLine/{}'.format(ApiUrl, stopId, lineId)
    if service is not None:
        resultUrl += '?serviceTypes={}'.format(service)
    result = requests.get(resultUrl)
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)

def getRouteSectionsForStopPoint (stopId, serviceType):
    if stopId is None:
        return Response("The given stop id was None", 422)
    resultUrl = '{}StopPoint/{}/Route'.format(ApiUrl, stopId)
    if serviceType is not None:
        resultUrl += '?serviceTypes={}'.format(serviceType)
    result = requests.get(resultUrl)
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)

def getDisruptionsForMode (mode, includeBlocked):
    if mode is None:
        return Response("The given mode was None", 422)
    if includeBlocked is None:
        includeBlocked = True
    result = requests.get('{}StopPoint/Mode/{}/Disruption?includeRouteBlockedStops={}'.format(ApiUrl, mode, includeBlocked))
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)

def getDisruptionsForStop (stopId, getFamily, includeRouteBlocked, flattenResponse):
    if stopId is None:
        return ("The given stop id was None", 422)
    if getFamily is None:
        getFamily = False
    if flattenResponse is True and getFamily is not True:
        flattenResponse = False
    resultUrl = '{}StopPoint/{}/Disruption'.format(ApiUrl, stopId)
    if getFamily is not None:
        resultUrl += '?getFamily={}'.format(getFamily)
    if includeRouteBlocked is not None:
        resultUrl += '&includeRouteBlockedStops={}'.format(includeRouteBlocked)
    if flattenResponse is not None:
        resultUrl += '&flattenResponse={}'.format(flattenResponse)
    result = requests.get(resultUrl)
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)

def getStopPointsWithinRadius (stopType, radius, modes, categories, getLines, lat, lon):
    if stopType is None or lat is None or lon is None:
        return Response("The given arguments are None", 422)
    if categories is None:
        categories = "none"
    if radius is None:
        radius = 200
    resultUrl = '{}StopPoint?stopTypes={}&radius={}&useStopPointHierarchy=true&categories={}&returnLines=true&location.lat={}&location.lon={}'.format(ApiUrl, stopType, radius, categories, lat, lon)
    if modes is not None:
        resultUrl += '&modes={}'.format(modes)
    result = requests.get(resultUrl)
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)

def getAllStopsByMode (mode, page):
    if mode is None:
        return Response("The given mode was None", 422)
    if page is None:
        page = 1
    result = requests.get('{}StopPoint/Mode/{}?page={}'.format(ApiUrl, mode, page))
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)

def searchStopPointsByQuery (queryString, modes, faresOnly, maxResults, lines, includeHubs, tflOnly):
    if queryString is None:
        return Response("The given query string was None", 422)
    if faresOnly is None:
        faresOnly = False
    if maxResults is None:
        maxResults = 1
    if includeHubs is None:
        includeHubs = True
    if tflOnly is None:
        tflOnly = False
    resultUrl = '{}StopPoint/Search?query={}&faresOnly={}&maxResults={}&includeHubs={}&tflOperatedNationalRailStationsOnly={}'.format(ApiUrl, queryString, faresOnly, maxResults, includeHubs, tflOnly)
    if modes is not None:
        resultUrl += '&modes={}'.format(modes)
    if lines is not None:
        resultUrl += '&lines={}'.format(lines)
    result = requests.get(resultUrl)
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)

def getCarParksAtStopPoint (stopId):
    if stopId is None:
        return Response("The given stop id was None", 422)
    result = requests.get('{}StopPoint/{}/CarParks'.format(ApiUrl, stopId))
    if (result is None or result == []):
        return Response("No result could be found", 422)
    if result.text[0] is '[':
        print("Trimming the '[]' characters from the JSON response")
        result.text = result.text[1:-1]
    return jsonify(result.text)