import requests
from flask import Flask, jsonify, current_app, Response, request
from Settings import ApiUrl, appid, appkey
from DatabaseAccess import InsertError

def getStopPointById (stopId, isCrowded):
    """ Returns a list of stop points filtered by station id
    Required:
        stopid is a single string representing the station to look from
    Optional:
        isCrowded is a boolean whether to include crowding information
    Example: 940GZZLUASL, true
    Note:
    URL: https://api.tfl.gov.uk/StopPoint/940GZZLUASL?includeCrowdingData=true&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if stopId is None:
            InsertError('stopId must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("The given stop id was None", 422)
        resultUrl = '{}StopPoint/{}?{}&{}'.format(ApiUrl, stopId, appid, appkey)
        if isCrowded is not None:
            resultUrl += '&includeCrowdingData={}'.format(isCrowded)
        result = requests.get(resultUrl)
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getStopPointByIdAndType (stopId, placeType):
    """ Returns a list of stop points filtered by station id and stop point type
    Required:
        stopid is a single string representing the station to look from
        type is an array or single string representing the type of stop point
    Optional:
    Example: 940GZZLUASL, NaptanMetroStation
    Note:
    URL: https://api.tfl.gov.uk/StopPoint/940GZZLUASL/placeTypes?placeTypes=NaptanMetroStation&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if stopId is None or placeType is None:
            InsertError('stopId must not be None, value was None. placeType must not be none, value was None.', 422, request.url, request.remote_addr)
            return Response("The given arguments are None", 422)
        result = requests.get('{}StopPoint/{}/placeTypes?placeTypes={}&{}&{}'.format(ApiUrl, stopId, placeType, appid, appkey))
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getCrowdingByIdAndLineAndDirection (stopId, lineId, direction):
    """ Returns crowding information based on the stop, line and direction of travel
    Required:
        stopid is a single string representing the station to look from
        lineid is a single string representing the line to check for crowding
    Optional:
        direction is a string, either 'all', 'inbound' or 'outbound' determining the direction of travel
    Example: 940GZZLUASL, piccadilly, all
    Note:
    URL: https://api.tfl.gov.uk/StopPoint/940GZZLUASL/Crowding/piccadilly?direction=inbound&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if stopId is None or lineId is None or direction is None:
            InsertError('stopId must not be None, value was None. lineId must not be None, value was None. direction must not be None, value was None.', 422, request.url, request.remote_addr)
            return Response("The given arguments are None", 422)
        result = requests.get('{}StopPoint/{}/Crowding/{}?direction={}&{}&{}'.format(ApiUrl, stopId, lineId, direction, appid, appkey))
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getStopsOfType (stopType):
    """ Returns services available at a stop point
    Required:
        stoptype is an array or single string representing the stop type to filter by
    Optional:
    Example: NaptanMetroStation
    Note: Maximum of 12 types
        NaptanMetroStation is a normal tube station, e.g. angel
    URL: https://api.tfl.gov.uk/StopPoint/Type/NaptanMetroStation?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if stopType is None:
            InsertError('stopType must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("The given argument was None", 422)
        result = requests.get('{}StopPoint/Type/{}?{}&{}'.format(ApiUrl, stopType, appid, appkey))
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getServicesForStop (stopId, lineId, serviceMode):
    """ Returns services available at a stop point
    Required:
        stopid is a single string representing a station
    Optional:
        lineid is an array or single string to limit results to only services on the specified lines
        mode is an array or single string limiting the results to only those within the given mode
    Example: 940GZZLUASL, piccadilly, tube
    Note: The URL provided by TFLs swagger file is incorrect
    URL: https://api.tfl.gov.uk/StopPoint/ServiceTypes?id=940GZZLUASL&lineIds=piccadilly&modes=tube&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if stopId is None:
            InsertError('stopId must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("The given stop id is None", 422)
        resultUrl = '{}StopPoint/ServiceTypes?id={}&{}&{}'.format(ApiUrl, stopId, appid, appkey)
        if lineId is not None:
            resultUrl += '&lineIds={}'.format(lineId)
        if serviceMode is not None:
            resultUrl += '&modes={}'.format(serviceMode)
        result = requests.get(resultUrl)
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getArrivalsByStopId (stopId):
    """ Returns arrivals at the given stop point
    Required:
        stopid is a single string representing a station
    Optional:
    Example: 940GZZLUASL
    Note: The URL provided by TFLs swagger file is incorrect
    URL: https://api.tfl.gov.uk/StopPoint/940GZZLUASL/Arrivals?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if stopId is None:
            InsertError('stopId must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("The given stop id is None", 422)
        result = requests.get('{}StopPoint/{}/Arrivals?{}&{}'.format(ApiUrl, stopId, appid, appkey))
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getStopsFromStationAndLine (stopId, lineId, service):
    """ Returns stop points reachable on the given line from the given stop point
    Required:
        stopid is a single string representing a station
        lineid is a single string representing a line
    Optional:
        servicetype is an array or single string for the type of service to return
    Example: 940GZZLUASL, piccadilly,  Regular
    Note: servicetype must be either 'Regular' or 'Night'
    URL: https://api.tfl.gov.uk/StopPoint/940GZZLUASL/CanReachOnLine/piccadilly?serviceTypes=Regular&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if stopId is None or lineId is None:
            InsertError('stopId must not be None, value was None. lineId must not be None, value was None.', 422, request.url, request.remote_addr)
            return Response("The given stop or line id was None", 422)
        resultUrl = '{}StopPoint/{}/CanReachOnLine/{}?{}&{}'.format(ApiUrl, stopId, lineId, appid, appkey)
        if service is not None:
            resultUrl += '&serviceTypes={}'.format(service)
        result = requests.get(resultUrl)
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getRouteSectionsForStopPoint (stopId, serviceType):
    """ Returns route sections for a stop point
    Required:
        stopid is a single string representing a station id
    Optional:
        servicetype is an array or single string for the type of service to return
    Example: 940GZZLUASL, Regular
    Note: servicetype must be either 'Regular' or 'Night'
    URL: https://api.tfl.gov.uk/StopPoint/940GZZLUASL/Route?serviceTypes=Regular&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if stopId is None:
            InsertError('stopId must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("The given stop id was None", 422)
        resultUrl = '{}StopPoint/{}/Route?{}&{}'.format(ApiUrl, stopId, appid, appkey)
        if serviceType is not None:
            resultUrl += '&serviceTypes={}'.format(serviceType)
        result = requests.get(resultUrl)
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getDisruptionsForMode (mode, includeBlocked):
    """ Returns disruption information based on the given mode
    Required:
        mode is an array or single string representing the mode to filter by
    Optional:
        includeblocked is a boolean whether to include blocked routes
    Example: tube, true
    URL: https://api.tfl.gov.uk/StopPoint/Mode/tube/Disruption?includeRouteBlockedStops=true&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if mode is None:
            InsertError('mode must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("The given mode was None", 422)
        if includeBlocked is None:
            includeBlocked = True
        result = requests.get('{}StopPoint/Mode/{}/Disruption?includeRouteBlockedStops={}&{}&{}'.format(ApiUrl, mode, includeBlocked, appid, appkey))
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getDisruptionsForStop (stopId, getFamily, includeRouteBlocked, flattenResponse):
    """ Returns disruption information based on the given stop point id
    Required:
        stopid is an array or single string representing stop points
    Optional:
        getfamily is a boolean whether to include disruptions for the whole family or just the given stop point
        includeblocked is a boolean whether to include blocked routes
        flatten is a boolean whether to associate all disruptions with parent stop point
    Example: 940GZZLUWYP, false, true, false
    Note: flatten is only used if getfamily is true
    URL: https://api.tfl.gov.uk/StopPoint/940GZZLUASL/Disruption?getFamily=true&includeRouteBlockedStops=true&flattenResponse=false&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if stopId is None:
            InsertError('stopId must not be None, value was None', 422, request.url, request.remote_addr)
            return ("The given stop id was None", 422)
        if getFamily is None:
            getFamily = False
        if flattenResponse is True and getFamily is not True:
            flattenResponse = False
        resultUrl = '{}StopPoint/{}/Disruption?{}&{}'.format(ApiUrl, stopId, appid, appkey)
        if getFamily is not None:
            resultUrl += '&getFamily={}'.format(getFamily)
        if includeRouteBlocked is not None:
            resultUrl += '&includeRouteBlockedStops={}'.format(includeRouteBlocked)
        if flattenResponse is not None:
            resultUrl += '&flattenResponse={}'.format(flattenResponse)
        result = requests.get(resultUrl)
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getStopPointsWithinRadius (stopType, radius, modes, categories, getLines, lat, lon):
    """ Returns information regarding stop points within an area
    Required:
        type is an array or single string for the type of stoppoint to filter
    Optional:
        radius is a string setting the distance, default is 200 if not provided
        mode is an array or string for the modes to filter by
        categories is an array or single string for 
        lines is a boolean whether to return line information or not
        lat is a string representing the latitude to be the centre point
        lon is a string represending the longitude to be the centre point
    Example: NaptanMetroStation, 400, tube, Toilets, central, 51.21, -0.21
    Note: categories is a very weird key value list, never got it working so it is ignored
        Initially the swagger URL included lat and lon with 'location.lon' and 'location.lat' instead but this did not work
    URL: https://api.tfl.gov.uk/StopPoint?stopTypes=NaptanMetroStation&radius=400&useStopPointHierarchy=true&modes=tube&returnLines=true&lat=51.21&lon=-0.21&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if stopType is None or lat is None or lon is None:
            InsertError('stopType must not be None, value was None. lat must not be None, value was None. lon must not be None, value was None.', 422, request.url, request.remote_addr)
            return Response("The given arguments are None", 422)
        if categories is None:
            categories = "none"
        if radius is None:
            radius = 200
        resultUrl = '{}StopPoint?stopTypes={}&radius={}&useStopPointHierarchy=true&categories={}&returnLines={}&lat={}&lon={}&{}&{}'.format(ApiUrl, stopType, radius, categories, getLines, lat, lon, appid, appkey)
        if modes is not None:
            resultUrl += '&modes={}'.format(modes)
        result = requests.get(resultUrl)
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getAllStopsByMode (mode, page):
    """ Returns information regarding stop points based on mode
    Required:
        mode is an array or single string to filter by
    Optional:
        page is an integer containing 1000 results per page in sequence, so
            1000 will include results 1-1000 and 2 will include 1001-2000
    Example: tube, 1 
    Note: page is required if the mode is set to 'bus'
    URL: https://api.tfl.gov.uk/StopPoint/Mode/tube?page=1&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if mode is None:
            InsertError('mode must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("The given mode was None", 422)
        if page is None:
            page = 1
        result = requests.get('{}StopPoint/Mode/{}?page={}&{}&{}'.format(ApiUrl, mode, page, appid, appkey))
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def searchStopPointsByQuery (queryString, modes, faresOnly, maxResults, lines, includeHubs, tflOnly):
    """ Returns information regarding stop points based on their name
    Required:
        query is a single string to search for stop points
    Optional:
        mode is an array or single string for a type of stop point
        faresonly is a boolean for including only stations that have fare data
        results is a string for result limit, default and limit is 50
        lines is an array or single string for lines to include in the filter
        includehubs is a boolean for including hubs such as Euston
        tflonly is a boolean for including tfl operated services
    Example: wembley, tube, true, 30, district, true, false
    Note: The example on the TFL swagger file has an incorrect URL
    URL: https://api.tfl.gov.uk/StopPoint/Search?query=wembley&modes=tube&faresOnly=true&maxResults=30&lines=district&includeHubs=true&tflOperatedNationalRailStationsOnly=false&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if queryString is None:
            InsertError('queryString must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("The given query string was None", 422)
        if faresOnly is None:
            faresOnly = False
        if maxResults is None:
            maxResults = 1
        if includeHubs is None:
            includeHubs = True
        if tflOnly is None:
            tflOnly = False
        resultUrl = '{}StopPoint/Search?query={}&faresOnly={}&maxResults={}&includeHubs={}&tflOperatedNationalRailStationsOnly={}&{}&{}'.format(ApiUrl, queryString, faresOnly, maxResults, includeHubs, tflOnly, appid, appkey)
        if modes is not None:
            resultUrl += '&modes={}'.format(modes)
        if lines is not None:
            resultUrl += '&lines={}'.format(lines)
        result = requests.get(resultUrl)
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)

def getCarParksAtStopPoint (stopId):
    """ Returns information regarding car parks at a stop point
    Required:
        stopid cannot be an array, must be a single string corresponding to a station Id
    Example: 940GZZLUWYP
    Note: The given URL on the TFL swagger API file is incorrect
    URL: https://api.tfl.gov.uk/StopPoint/940GZZLUWYP/CarParks?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if stopId is None:
            InsertError('stopId must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("The given stop id was None", 422)
        result = requests.get('{}StopPoint/{}/CarParks?{}&{}'.format(ApiUrl, stopId, appid, appkey))
        if (result is None or result == []):
            InsertError('result must not be None, value was None', 422, request.url, request.remote_addr)
            return Response("No result could be found", 422)
        return jsonify(result.text)