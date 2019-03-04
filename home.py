from flask import Flask, jsonify, json, request, Response
from flask_sslify import SSLify
import sys
import pdb

sys.path.append('/home/pi/Documents/FlaskAPI/TFLAPIScripts')
from Line import getLinesByMode, getArrivalsForLineAndStop, getLineStatus, getLineById, getLineByIdAndService, getLineInfoByDateAndId, getLineStatusbyId, getLinesBySeverityCode, getLineStatusByMode, getSequenceOnRoute, getStationsOnLine, getTimetableForStationOnLine, getTimetableForJourney, getDisruptionsForGivenLine, getDisruptionsForGivenMode
from BikePoint import getBikePointById, getBikePoints, getBikePointByQuery
from Occupancy import getBikePointOccupancyById, getCarParkOccupancyById, getChargeConnectorById
from Place import getPlaceById, getPlaceByName, getPlacesByBoundingbox, getPlacesByTypeAndStatus
from StopPoint import searchStopPointsByQuery, getAllStopsByMode, getArrivalsByStopId, getCarParksAtStopPoint, getCrowdingByIdAndLineAndDirection, getDisruptionsForMode, getDisruptionsForStop, getRouteSectionsForStopPoint, getServicesForStop, getStopPointById, getStopPointByIdAndType, getStopPointsWithinRadius, getStopsFromStationAndLine, getStopsOfType
from DatabaseAccess import InsertError, InsertRequest

app = Flask(__name__)
sslify = SSLify(app)

@app.route('/')
def checkStatus():
    return 'Hello, World!'

@app.route('/Line/getAllLineStatus', methods=['GET'])
def getAllLineStatus():
    """ Returns a list of all tube and dlr lines and their statuses
    Required:
    Optional:
    Example:
    Note: The URL given by the TFL documentation does not work
    """

    result = getLineStatus()
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Line/getLinesById', methods=['GET'])
def getLinesById():
    """ Returns a list of lines that match the given line id
    Required:
        id is an array or single string representing the line id to search for
    Optional:
    Example: piccadilly
    Note: The URL given by the TFL documentation does not work
    """

    id = request.args.get('id', default=None, type=str)
    if type(id) is not str:
        InsertError('id must be string, value was {}'.format(type(id)), 422, request.url, request.remote_addr)
        return Response("The given Id was not a string", 422)
    result = getLineById(id)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Line/getByMode', methods=['GET'])
def getLineByMode():
    """ Returns a list of lines in the given mode
    Required:
        mode is an array or single string representing the given modes lines can runs on
    Optional:
    Example: tube
    Note: The URL given by the TFL documentation does not work
    """

    mode = request.args.get('mode', default = None, type = str)
    if type(mode) is not str:
        InsertError('mode must be string, value was {}'.format(type(mode)), 422, request.url, request.remote_addr)
        return Response("The given mode was not a string", 422)
    result = getLinesByMode(mode)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Line/getByServiceAndId', methods=['GET'])
def getLineByServiceAndId():
    """ Returns a list of valid routes for the given lineids and service type
    Required:
        id is an array or single string representing the id of the lines to query
        service is an array or single string representing the type of service to search for
    Optional:
    Example: piccadilly, Regular
    Note: The URL given by the TFL documentation does not work
        If not provided the API defaults to Regular anyway
    """

    service = request.args.get('service',default="Regular",type=str)
    id = request.args.get('id',default=None,type=str)

    if service == "":
        service = "Regular"
    if type(id) is not str:
        InsertError('id must be string, value was {}'.format(type(id)), 422, request.url, request.remote_addr)
        return Response("The given id was not a string", 422)
    if service is not None and type(service) is not str:
        InsertError('service must be string, value was {}'.format(type(service)), 422, request.url, request.remote_addr)
        return Response("The given service was not a string", 422)
    result = getLineByIdAndService(id, service)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Line/getLineByDateAndId', methods=['GET'])
def getLineByDateAndId():
    """ Returns a list of lines with their status based on the given ids and date range
    Required:
        id is an array or single string representing the id of the lines to query
        start is a single string and is the start date of the query daterange
        end is a single string and is the end date of the query daterange 
    Optional:
    Example: piccadilly, 2018-12-06T13:36:56, 2018-12-09T13:36:56
    Note: The URL given by the TFL documentation does not work
        The 'true' parameter is always true as I always want a detailed return statement 
    """

    id = request.args.get('id', default = None, type = str)
    start = request.args.get('start', default = None, type = str)
    end = request.args.get('end', default = None, type = str)
    if type(id) is not str or type(start) is not str or type(end) is not str:
        InsertError('id must be string, value was {}. start must be string, value was {}. end must be string, value was {}'.format(type(id), type(start), type(end)), 422, request.url, request.remote_addr)
        return Response("Parameters must be string", 422)
    result = getLineInfoByDateAndId(id, start, end, "true")
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Line/getLineStatusById', methods=['GET'])
def getStatusById():
    """ Returns a list of lines with their status based on the given ids
    Required:
        id is an array or single string representing the id of the lines to query
    Optional:
    Example: piccadilly
    Note: The URL given by the TFL documentation does not work
        The 'true' parameter is always true as I always want a detailed return statement 
    """

    id = request.args.get('id', default = None, type = str)
    if type(id) is not str:
        InsertError('id must be string, value was {}'.format(type(id)), 422, request.url, request.remote_addr)
        return Response("The id must be of type string", 422)
    result = getLineStatusbyId(id, "true")
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result
    
@app.route('/Line/getLineBySeverity', methods=['GET'])
def getLineBySeverity():
    """ Returns a list of all lines matching the given severity code
    Required:
        severity is a single string between 0 and 14, inclusive, representing the severity on that line 
    Optional:
    Example: 9
    Note: The URL given by the TFL documentation does not work
    """

    severity = request.args.get('severitycode', default = None, type = str)
    if type(severity) is not str:
        InsertError('severity must be string, value was {}'.format(type(severity)), 422, request.url, request.remote_addr)
        return Response("Severity code must be of type string", 422)
    result = getLinesBySeverityCode(severity)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Line/getLineStatusByMode', methods=['GET'])
def getLineStatusByModes():
    """ Returns a list of all line statuses based on the mode
    Required:
        mode is an array or a single string representing the mode(s) to get results for
    Optional:
    Example: tube, true
    Note: The URL given by the TFL documentation does not work
        The 'true' string within the api call is to always include detail within the response
    """

    mode = request.args.get('mode', default = None, type = str)
    if type(mode) is not str:
        InsertError('mode must be string, value was {}'.format(type(mode)), 422, request.url, request.remote_addr)
        return Response("Mode must be of type string", 422)
    result = getLineStatusByMode(mode, "true")
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result
    
@app.route('/Line/getStationsOnLineById', methods=['GET'])
def getStationsOnLineById():
    """ Returns a list of stations that serve the given line id
    Required:
        lineid is a single string representing the line to get stations on
    Optional:
    Example: piccadilly, true
    Note: The URL given by the TFL documentation does not work
        The 'false' string within the api call is to not filter out any non-tfl stations
    """

    id = request.args.get('id', default = None, type = str)
    if type(id) is not str:
        InsertError('id must be string, value was {}'.format(type(id)), 422, request.url, request.remote_addr)
        return Response("The given id must be of type string", 422)
    result = getStationsOnLine(id, "false")
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Line/getSequenceOfStopsOnRoute', methods=['GET'])
def getSequenceOfStopsOnRoute():
    """ Returns a list of stations on a route
    Required:
        id is a single string representing the line to get stations on
        direction is a single string of inbound or outbound
    Optional:
    serviceTypes is a single string or array specifying either Regular or Night service
    Example: victoria, inbound, Regular
    Note:
    """

    id = request.args.get('id', default = None, type = str)
    direction = request.args.get('direction', default = "inbound", type = str)
    serviceTypes = request.args.get('servicetype', default = "Regular", type = str)

    if type(id) is not str:
        InsertError('id must be string, value was {}'.format(type(id)), 422, request.url, request.remote_addr)
        return Response("The given id must be of type string", 422)
    if type(direction) is not str or (direction != "inbound" and direction != "outbound"):
        direction = "inbound"
    if serviceTypes != "Regular" and serviceTypes != "Night":
        serviceTypes = "Regular"
    result = getSequenceOnRoute(id, direction, serviceTypes, "false")
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Line/getTimetableForStationOnLine', methods=['GET'])
def getTimetableForStationOnLineByStationIdLineId():
    """ Returns a timetable for a journey based on source station id and the line id
    Required:
        stationid is a single string representing the source station id
        lineid is a single string representing the line to get a timetable for
    Optional:
    Example: 940GZZLUASL, piccadilly
    Note: The URL given by the TFL documentation does not work
    """

    stationid = request.args.get('stationid', default = None, type = str)
    lineid = request.args.get('lineid', default = None, type = str)
    if type(stationid) is not str or type(lineid) is not str:
        InsertError('stationid must be string, value was {}. lineid must be string, value was {}'.format(type(stationid), type(lineid)), 422, request.url, request.remote_addr)
        return Response("The station id and line id must be of type string", 422)
    result = getTimetableForStationOnLine(stationid, lineid)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Line/getTimetableForJouneyBySourceIdDestIdLineId', methods=['GET'])
def getTimetableForJouneyBySourceIdDestIdLineId():
    """ Returns a timetable for a journey based on source station id, destination station id and the line id
    Required:
        sourceid is a single string representing the source station id
        destid is a single string representing the destination station id  
        lineid is a single string representing the line to get a timetable for
    Optional:
    Example: 940GZZLUASL, 940GZZLUASG, piccadilly
    Note: The URL given by the TFL documentation does not work
    """
    
    sourceid = request.args.get('sourceid', default = None, type = str)
    destid = request.args.get('destid', default = None, type = str)
    lineid = request.args.get('lineid', default = None, type = str)
    if type(sourceid) is not str or type(destid) is not str or type(lineid) is not str:
        InsertError('sourceid must be string, value was {}. destid must be string, value was {}. lineid must be string, value was {}'.format(type(sourceid), type(destid), type(lineid)), 422, request.url, request.remote_addr)
        return Response("The source id, destination id and line id must be of type string", 422)
    result = getTimetableForJourney(sourceid, destid, lineid)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Line/getDisruptionsByLineId', methods=['GET'])
def getDisruptionsByLineId():
    """ Returns information about arrival predictions based on a line id
    Required:
        lineid is an array or single string representing the line to get disruptions for
    Optional:
    Example: waterloo
    Note: The URL given by the TFL documentation does not work
    """

    lineid = request.args.get('lineid', default = None, type = str)
    if type(lineid) is not str:
        InsertError('lineid must be string, value was {}'.format(type(lineid)), 422, request.url, request.remote_addr)
        return Response("The given line id musy be of type string", 422)
    result = getDisruptionsForGivenLine(lineid)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Line/getDisruptionsByMode', methods=['GET'])
def getDisruptionsByMode():
    """ Returns information about arrival predictions based on a given mode
    Required:
        mode is an array or single string representing the mode of travel
    Optional:
    Example: tube
    Note: The URL given by the TFL documentation does not work
    """

    mode = request.args.get('mode', default = None, type = str)
    if type(mode) is not str:
        InsertError('mode must be string, value was {}'.format(type(mode)), 422, request.url, request.remote_addr)
        return Response("The given mode must be of type string", 422)
    result = getDisruptionsForGivenMode(mode)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Line/getArrivalsForLineAndStop', methods=['GET'])
def getArrivalsForLineAndStation():
    """ Returns information about arrival predictions based on a line id and stop id
    Required:
        lineid is an array or single string for the line(s) to predict arrivals on
        source is a single string for the stop point to get arrival predictions for
    Optional:
        dest is a single string representing the destination of the arrivals
        direction is a string representing the direction of travel, can be 'inbound', 'outbound' or 'all'
    Example: piccadilly, 940GZZLUASL, 940GZZLUASL, all 
    Note: The URL given by the TFL documentation does not work
        The swagger file says stop point id is both optional and required, but it is required
        The included example does not work as not sure whether dest is optional or not
    """

    lineid = request.args.get('lineid', default = None, type = str)
    source = request.args.get('source', default = None, type = str)
    dest = request.args.get('dest', default = None, type = str)
    direction = request.args.get('direction', default = "all", type = str)
    if type(lineid) is not str or type(source) is not str:
        InsertError('lineid must be string, value was {}. source must be string, value was {}'.format(type(lineid), type(source)), 422, request.url, request.remote_addr)
        return Response("The line id and source id must be of type string", 422)
    if dest == "":
        dest = None
    if direction == "":
        direction = None
    if dest is not None:
        if type(dest) is not str:
            InsertError('dest must be string, value was {}'.format(type(dest)), 422, request.url, request.remote_addr)
            return Response("The destination if given must be of type string", 422)
    if direction is not None:
        if type(direction) is not str:
            InsertError('direction must be string, value was {}'.format(type(direction)), 422, request.url, request.remote_addr)
            return Response("The direction if given must be of type string", 422)
        direction = direction.lower()
        if direction != "inbound" and direction != "outbound" and direction != "all":
            InsertError('direction must be inbound, outbound or all, value was {}'.format(direction), 422, request.url, request.remote_addr)
            return Response("The given direction must be: outbound, inbound or all", 422)
    result = getArrivalsForLineAndStop(lineid, source, dest, direction)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Bike/getBikePoints', methods=['GET'])
def getAllBikePoints():
    """ Returns information about all bike points
    Required:
    Optional:
    Example:
    Note: The URL given by the TFL documentation does not work
    """

    result = getBikePoints()
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Bike/getBikePointById', methods=['GET'])
def getBikePointsById():
    """ Returns information about a bike point based on the id
    Required:
        id is a single string representing the bikepoints id
    Optional:
    Example: BikePoints_1
    Note: The URL given by the TFL documentation does not work
    """

    id = request.args.get('id', default = None, type = str)
    if type(id) is not str:
        InsertError('id must be string, value was {}'.format(type(id)), 422, request.url, request.remote_addr)
        return Response("The given id must be of type string", 422)
    result = getBikePointById(id)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Bike/getBikePointByQuery', methods=['GET'])
def getBikePointsByQuery():
    """ Returns information about a bike point based on the search query
    Required:
        query is a single string representing the search term
    Optional:
    Example: St. James
    Note: The URL given by the TFL documentation does not work
    """

    query = request.args.get('query', default = None, type = str)
    if type(query) is not str:
        InsertError('query must be string, value was {}'.format(type(query)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getBikePointByQuery(query)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Occupancy/getCarParkById', methods=['GET'])
def getCarParkById():
    """ Returns occupancy of a carpark based on the id
    Required:
        id is a single string for the car park id to search for
    Optional:
    Example: CarParks_800477
    Note: The URL given by the TFL documentation does not work
    """

    id = request.args.get('id', default = None, type = str)
    if type(id) is not str:
        InsertError('id must be string, value was {}'.format(type(id)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getCarParkOccupancyById(id)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Occupancy/getChargeById', methods=['GET'])
def getChargeById():
    """ Returns occupancy of a charge point based on the id
    Required:
        id is an array or single string for the charge point id to search for
    Optional:
    Example: BikePoints_1
    Note: The URL given by the TFL documentation does not work
    """

    id = request.args.get('id', default = None, type = str)
    if type(id) is not str:
        InsertError('id must be string, value was {}'.format(type(id)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getChargeConnectorById(id)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Occupancy/getBikePointById', methods=['GET'])
def getConnectorById():
    """ Returns occupancy of a bikepoint based on the id
    Required:
        id is an array or single string for the bikepoint id to search for
    Optional:
    Example: BikePoints_1
    Note: The URL given by the TFL documentation does not work
    """

    id = request.args.get('id', default = None, type = str)
    if type(id) is not str:
        InsertError('id must be string, value was {}'.format(type(id)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getBikePointOccupancyById(id)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Place/GetPlaceByTypeAndStatus', methods=['GET'])
def getPlaceByTypeAndStatus():
    """ Returns places that match the type
    Required:
        type is the type of place to return
    Optional:
        activeOnly is a boolean whether to include only active places
    Example: BikePoint, true
    Note: The URL given by the TFL documentation does not work
        activeonly usually returns no results if set to false, not sure if based on closing times
    """

    placeType = request.args.get('type', default = None, type = str)
    activeOnly = request.args.get('activeonly', default = None, type = str)
    if type(placeType) is not str or type(activeOnly) is not str:
        InsertError('placeType must be string, value was {}. activeOnly must be string, value was {}'.format(type(placeType), type(activeOnly)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getPlacesByTypeAndStatus(placeType, activeOnly)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Place/GetPlaceById', methods=['GET'])
def getPlacesById():
    """ Returns places that match the place id
    Required:
        id is a single string representing the id of a place
    Optional:
    Example: BikePoints_1, true
    Note: The URL given by the TFL documentation does not work
        Another parameter 'includechildren' is always true so has been hard coded in
    """
    
    id = request.args.get('id', default = None, type = str)
    if type(id) is not str:
        InsertError('id must be string, value was {}'.format(type(id)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getPlaceById(id, "true")
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Place/GetPlaceByBounds', methods=['GET'])
def getPlacesByBounds():
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
    """

    placeType = request.args.get('type', default = None, type = str)
    categories = request.args.get('categories', default = None, type = str)
    includeChildren = request.args.get('includechildren', default = "true", type = str)
    activeOnly = request.args.get('activeonly', default = "false", type=str)
    swlat = request.args.get('swlat', default = None, type = str)
    swlon = request.args.get('swlon', default = None, type = str)
    nelat = request.args.get('nelat', default = None, type = str)
    nelon = request.args.get('nelon', default = None, type = str)
    
    if placeType == "":
        placeType = None
    if categories == "":
        categories = None
    if includeChildren == "":
        includeChildren = "true"
    if activeOnly == "":
        activeOnly = "false"
    if type(swlat) is not str or type(swlon) is not str or type(nelat) is not str or type(nelon) is not str:
        InsertError('swlat must be string, value was {}. swlon must be string, value was {}. nelat must be string, value was {}. nelon must be string, value was {}.'.format(type(swlat), type(swlon), type(nelat), type(nelon)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getPlacesByBoundingbox(categories, includeChildren, placeType, activeOnly, swlat, swlon, nelat, nelon)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/Place/GetPlaceByName', methods=['GET'])
def getPlacesByName():
    """ Returns a list of places filtered by name
    Required:
        name is a single string representing the name of a place
    Optional:
        type is an array or single string representing the type of place to search for 
    Example: Brent Cross Stn (LUL), CarPark
    Note: The URL given by the TFL documentation does not work
    """

    name = request.args.get('name', default = None, type = str)
    placeType = request.args.get('type', default = None, type = str)

    if placeType == "":
        placeType = None

    if type(name) is not str:
        InsertError('name must be string, value was {}'.format(type(name)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getPlaceByName(name, placeType)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/StopPoint/GetStopPointById', methods=['GET'])
def getStopPointInfoById():
    """ Returns a list of stop points filtered by station id
    Required:
        stopid is a single string representing the station to look from
    Optional:
        isCrowded is a boolean whether to include crowding information
    Example: 940GZZLUASL, true
    Note: 
    """

    id = request.args.get('id', default = None, type = str)
    crowded = request.args.get('isCrowded', default = "true", type = str)

    if crowded == "":
        crowded = "true"

    if type(id) is not str:
        InsertError('id must be string, value was {}'.format(type(id)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getStopPointById(id, crowded)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/StopPoint/GetStopPointByIdAndType', methods=['GET'])
def getStopPointInfoByIdAndType():
    """ Returns a list of stop points filtered by station id and stop point type
    Required:
        stopid is a single string representing the station to look from
        type is an array or single string representing the type of stop point
    Optional:
    Example: 940GZZLUASL, NaptanMetroStation
    Note: 
    """

    stopid = request.args.get('id', default = None, type = str)
    placeType = request.args.get('type', default = None, type = str)
    if type(stopid) is not str or type(placeType) is not str:
        InsertError('stopid must be string, value was {}. placeType must be a string, value was {}'.format(type(stopid), type(placeType)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getStopPointByIdAndType(stopid, placeType)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/StopPoint/GetCrowdingByStopLineDirection', methods=['GET'])
def getCrowdingByStopLineDirection():
    """ Returns crowding information based on the stop, line and direction of travel
    Required:
        stopid is a single string representing the station to look from
        lineid is a single string representing the line to check for crowding
    Optional:
        direction is a string, either 'all', 'inbound' or 'outbound' determining the direction of travel
    Example: 940GZZLUASL, piccadilly, all
    Note: direction is needed for the api call, but there is handling here for if it is missing
    """

    stopid = request.args.get('stopid', default = None, type = str)
    lineid = request.args.get('lineid', default = None, type = str)
    direction = request.args.get('direction', default = "all", type = str)
    
    if direction == "" or (direction.lower() != "inbound" and direction.lower() != "outbound"):
        direction = "all"
    
    direction = direction.lower()

    if stopid is None or lineid is None:
        InsertError('lineid must be string, value was {}'.format(type(lineid)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422) 

    result = getCrowdingByIdAndLineAndDirection(stopid, lineid, direction)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/StopPoint/GetStopByType', methods=['GET'])
def getStopByType():
    """ Returns services available at a stop point
    Required:
        stoptype is an array or single string representing the stop type to filter by
    Optional:
    Example: NaptanMetroStation
    Note: Maximum of 12 types
        NaptanMetroStation is a normal tube station, e.g. angel
    """

    stopType = request.args.get('type', default = None, type = str)
    if type(stopType) is not str:
        InsertError('stopType must be string, value was {}'.format(type(stopType)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getStopsOfType(stopType)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/StopPoint/GetServicesForStop', methods=['GET'])
def getServicesForStopPoint():
    """ Returns services available at a stop point
    Required:
        stopid is a single string representing a station
    Optional:
        lineid is an array or single string to limit results to only services on the specified lines
        mode is an array or single string limiting the results to only those within the given mode
    Example: 940GZZLUASL, piccadilly, tube
    Note: The URL provided by TFLs swagger file is incorrect
    """

    stopid = request.args.get('stopid', default = None, type = str)
    lineid = request.args.get('lineid', default = None, type = str)
    mode = request.args.get('mode', default = None, type = str)

    if lineid == "":
        lineid = None
    if mode == "":
        mode = None
    
    if type(stopid) is not str:
        InsertError('stopid must be string, value was {}'.format(type(stopid)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getServicesForStop(stopid, lineid, mode)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/StopPoint/GetArrivalsForStop', methods=['GET'])
def getArrivalsForStopPoint():
    """ Returns arrivals at the given stop point
    Required:
        stopid is a single string representing a station
    Optional:
    Example: 940GZZLUASL
    Note: The URL provided by TFLs swagger file is incorrect
    """

    stopid = request.args.get('stopid', default = None, type = str)
    if type(stopid) is not str:
        InsertError('stopid must be string, value was {}'.format(type(stopid)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getArrivalsByStopId(stopid)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/StopPoint/GetStopsOnLineFromStop', methods=['GET'])
def getStopsOnLineFromStop():
    """ Returns stop points reachable on the given line from the given stop point
    Required:
        stopid is a single string representing a station
        lineid is a single string representing a line
    Optional:
        servicetype is an array or single string for the type of service to return
    Example: 940GZZLUASL, piccadilly,  Regular
    Note: servicetype must be either 'Regular' or 'Night'
    """

    stopid = request.args.get('stopid', default = None, type = str)
    lineid = request.args.get('lineid', default = None, type = str)
    serviceType = request.args.get('servicetype', default = "Regular", type = str)

    if serviceType == "regular":
        serviceType = "Regular"
    if serviceType == "night":
        serviceType = "Night"

    if serviceType == "" or serviceType.lower() != "regular" or serviceType.lower() != "night":
        serviceType = "Regular"

    if type(stopid) is not str or type(lineid) is not str:
        InsertError('lineid must be string, value was {}'.format(type(lineid)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getStopsFromStationAndLine(stopid, lineid, serviceType)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/StopPoint/GetRouteSectionsFromStop', methods=['GET'])
def getRouteSectionsfromStop():
    """ Returns route sections for a stop point
    Required:
        stopid is a single string representing a station id
    Optional:
        servicetype is an array or single string for the type of service to return
    Example: 940GZZLUASL, Regular
    Note: servicetype must be either 'Regular' or 'Night'
    """

    stopid = request.args.get('stopid', default = None, type = str)
    serviceType = request.args.get('servicetype', default = "Regular", type = str)
    
    if serviceType == "" or serviceType.lower() != "regular" or serviceType.lower() != "night":
        serviceType = "Regular"

    if type(stopid) is not str:
        InsertError('stopid must be string, value was {}'.format(type(stopid)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getRouteSectionsForStopPoint(stopid, serviceType)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/StopPoint/GetDisruptionsForMode', methods=['GET'])
def getDisruptionsOnMode():
    """ Returns disruption information based on the given mode
    Required:
        mode is an array or single string representing the mode to filter by
    Optional:
        includeblocked is a boolean whether to include blocked routes
    Example: tube, true
    """

    servicemode = request.args.get('mode', default = None, type = str)
    includeblocked = request.args.get('includeblocked', default = "true", type = str)
    
    if includeblocked == "":
        includeblocked = "true"

    if type(servicemode) is not str:
        InsertError('servicemode must be string, value was {}'.format(type(servicemode)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getDisruptionsForMode(servicemode, includeblocked)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/StopPoint/GetDisruptionsForStopPoint', methods=['GET'])
def getDisruptionsForStopPoint():
    """ Returns disruption information based on the given stop point id
    Required:
        stopid is an array or single string representing stop points
    Optional:
        getfamily is a boolean whether to include disruptions for the whole family or just the given stop point
        includeblocked is a boolean whether to include blocked routes
        flatten is a boolean whether to associate all disruptions with parent stop point
    Example: 940GZZLUWYP, false, true, false
    Note: flatten is only used if getfamily is true
    """

    stopid = request.args.get('stopid', default = None, type = str)
    getfamily = request.args.get('getfamily', default = "false", type = str)
    includeblocked = request.args.get('includeblocked', default = "true", type = str)
    flatten = request.args.get('flatten', default = None, type = str)

    if getfamily == "":
        getfamily = "false"
    if includeblocked == "":
        includeblocked = "true"
    if getfamily is None or getfamily is "false":
        flatten = "false"
    else:
        if flatten is "false" or flatten is "":
            flatten = "false"
        else:
            flatten = "true"
    
    if type(stopid) is not str:
        InsertError('stopid must be string, value was {}'.format(type(stopid)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getDisruptionsForStop(stopid, getfamily, includeblocked, flatten)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/StopPoint/GetStopsWithinRadius', methods=['GET'])
def getStopsWithinRadius():
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
    Example: NaptanMetroStation, 400, tube, Toilets, true, 51.21, -0.21
    Note: categories is a very weird key value list, never got it working so it is ignored
    """

    stopType = request.args.get('type', default = None, type = str)
    radius = request.args.get('radius', default = 200, type = str)
    mode = request.args.get('mode', default = None, type = str)
    categories = request.args.get('categories', default = None, type = str)
    includelines = request.args.get('lines', default = "true", type = str)
    lat = request.args.get('lat', default = None, type = str)
    lon = request.args.get('lon', default = None, type = str)

    if radius == "":
        radius = 200
    if mode == "":
        mode = None
    if categories == "":
        categories = None
    if includelines == "":
        includelines = "true"

    if type(stopType) is not str or type(lat) is not str or type(lon) is not str:
        InsertError('stopType must be string, value was {}. lat must be str, value was {}. lon must be str, value was {}.'.format(type(stopType), type(lat), type(lon)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getStopPointsWithinRadius(stopType, radius, mode, categories, includelines, lat, lon)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/StopPoint/GetStopsByMode', methods=['GET'])
def getStopsByMode():
    """ Returns information regarding stop points based on mode
    Required:
        mode is an array or single string to filter by
    Optional:
        page is an integer containing 1000 results per page in sequence, so
            1000 will include results 1-1000 and 2 will include 1001-2000
    Example: tube, 1 
    Note: page is required if the mode is set to 'bus'
    """

    servicemode = request.args.get('mode', default = None, type = str)
    page = request.args.get('page', default = "1", type = str)
    if page == "" or page is None:
        page = "1"
    print(servicemode)
    if type(servicemode) is not str:
        InsertError('servicemode must be string, value was {}'.format(type(servicemode)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getAllStopsByMode(servicemode, page)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/StopPoint/GetStopPointsByQuery', methods=['GET'])
def getStopsByQuery():
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
    """

    query = request.args.get('query', default = None, type = str)
    modes = request.args.get('mode', default = None, type = str)
    faresOnly = request.args.get('faresonly', default = "false", type = str)
    results = request.args.get('results', default = "50", type = str)
    lines = request.args.get('lines', default = None, type = str)
    includeHubs= request.args.get('includehubs', default = "true", type = str)
    tflOnly = request.args.get('tflonly', default = "false", type = str)

    if modes == "":
        modes = None
    if faresOnly == "":
        faresOnly = "false"
    if results == "":
        results = "50"
    if lines == "":
        lines = None
    if includeHubs == "":
        includeHubs = "true"
    if tflOnly == "":
        tflOnly = "false"

    if type(query) is not str:
        InsertError('query must be string, value was {}'.format(type(query)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = searchStopPointsByQuery(query, modes, faresOnly, results, lines, includeHubs, tflOnly)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result

@app.route('/StopPoint/GetCarParksAtStopPoint', methods=['GET'])
def getCarParksAtStop():
    """ Returns information regarding car parks at a stop point
    Required:
        stopid cannot be an array, must be a single string corresponding to a station Id
    Example: 940GZZLUWYP
    """

    stopid = request.args.get('stopid', default = None, type = str)
    if type(stopid) is not str:
        InsertError('stopid must be string, value was {}'.format(type(stopid)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = getCarParksAtStopPoint(stopid)
    InsertRequest(request.url, request.method, request.remote_addr, result.json)
    return result