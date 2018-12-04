from flask import Flask, jsonify, json, request, Response
from flask_sslify import SSLify
import sys
sys.path.append('/home/pi/Documents/FlaskAPI/TFLAPIScripts')
from Line import *
from BikePoint import *
from Occupancy import *
from Place import *
from StopPoint import *
from test import *
app = Flask(__name__)
sslify = SSLify(app)

@app.route('/')
def checkStatus():
    return 'Hello, World!'

@app.route('/Line/getAllLineStatus', methods=['GET'])
def getAllLineStatus():
    result = getLineStatus()
    return result

@app.route('/Line/getLinesById', methods=['GET'])
def getLinesById():
    Id = request.args.get('id', default=None, type=str)
    if type(Id) is not str:
        return Response("The given Id was not a string", 422)
    result = getLineById(Id)
    return result

@app.route('/Line/getByMode', methods=['GET'])
def getLineByMode():
    mode = request.args.get('mode', default = None, type = str)
    if type(mode) is not str:
        return Response("The given mode was not a string", 422)
    result = getLinesByMode(mode)
    return result

@app.route('/Line/getByServiceAndId', methods=['GET'])
def getLineByServiceAndId():
    service = request.args.get('service',default=None,type=str)
    id = request.args.get('id',default=None,type=str)
    if type(id) is not str:
        return Response("The given id was not a string", 422)
    if service is not None and type(service) is not str:
        return Response("The given service was not a string", 422)
    result = getLineByIdAndService(id, service)
    return result

@app.route('/Line/getLineByDateAndId', methods=['GET'])
def getLineByDateAndId():
    id = request.args.get('id', default = None, type = str)
    start = request.args.get('start', default = None, type = str)
    end = request.args.get('end', default = None, type = str)
    if type(id) is not str or type(start) is not str or type(end) is not str:
        return Response("Parameters must be string", 422)
    result = getLineInfoByDateAndId(id, start, end, "true")
    return result

@app.route('/Line/getLineStatusById', methods=['GET'])
def getStatusById():
    id = request.args.get('id', default = None, type = str)
    if type(id) is not str:
        return Response("The id must be of type string", 422)
    result = getLineStatusbyId(id, "true")
    return result
    
@app.route('/Line/getLineBySeverity', methods=['GET'])
def getLineBySeverity():
    severity = request.args.get('severitycode', default = None, type = str)
    if type(severity) is not str:
        return Response("Severity code must be of type string", 422)
    result = getLinesBySeverityCode(severity)
    return result

@app.route('/Line/getLineStatusByMode', methods=['GET'])
def getLineStatusByModes():
    mode = request.args.get('mode', default = None, type = str)
    if type(mode) is not str:
        return Response("Mode must be of type string", 422)
    result = getLineStatusByMode(mode, "true")
    return result
    
@app.route('/Line/getStationsOnLineById', methods=['GET'])
def getStationsOnLineById():
    id = request.args.get('id', default = None, type = str)
    if type(id) is not str:
        return Response("The given id must be of type string", 422)
    result = getStationsOnLine(id, "true")
    return result

@app.route('/Line/getTimetableForStationOnLine', methods=['GET'])
def getTimetableForStationOnLineByStationIdLineId():
    stationid = request.args.get('stationid', default = None, type = str)
    lineid = request.args.get('lineid', default = None, type = str)
    if type(stationid) is not str or type(lineid) is not str:
        return Response("The station id and line id must be of type string", 422)
    result = getTimetableForStationOnLine(stationid, lineid)
    return result

@app.route('/Line/getTimetableForJouneyBySourceIdDestIdLineId', methods=['GET'])
def getTimetableForJouneyBySourceIdDestIdLineId():
    sourceid = request.args.get('sourceid', default = None, type = str)
    destid = request.args.get('destid', default = None, type = str)
    lineid = request.args.get('lineid', default = None, type = str)
    if type(sourceid) is not str or type(destid) is not str or type(lineid) is not str:
        return Response("The source id, destination id and line id must be of type string", 422)
    result = getTimetableForJourney(sourceid, destid, lineid)
    return result

@app.route('/Line/getDisruptionsByLineId', methods=['GET'])
def getDisruptionsByLineId():
    lineid = request.args.get('lineid', default = None, type = str)
    if type(lineid) is not str:
        return Response("The given line id musy be of type string", 422)
    result = getDisruptionsForGivenLine(lineid)
    return result

@app.route('/Line/getDisruptionsByMode', methods=['GET'])
def getDisruptionsByMode():
    mode = request.args.get('mode', default = None, type = str)
    if type(mode) is not str:
        return Response("The given mode must be of type string", 422)
    result = getDisruptionsForGivenMode(mode)
    return result

@app.route('/Line/getArrivalsForLineAndStop', methods=['GET'])
def getArrivalsForLineAndStation():
    lineid = request.args.get('lineid', default = None, type = str)
    source = request.args.get('source', default = None, type = str)
    dest = request.args.get('dest', default = None, type = str)
    direction = request.args.get('direction', default = None, type = str)
    if type(lineid) is not str or type(source) is not str:
        return Response("The line id and source id must be of type string", 422)
    if dest is not None:
        if type(dest) is not str:
            return Response("The destination if given must be of type string", 422)
    if direction is not None:
        if type(direction) is not str:
            return Response("The direction if given must be of type string", 422)
        if direction is not "inbound" or direction is not "outbound" or direction is not "all":
            return Response("The given direction must be: outbound, inbound or all", 422)
    result = getArrivalsForLineAndStop(lineid, source, dest, direction)
    return result

@app.route('/Bike/getBikePoints', methods=['GET'])
def getAllBikePoints():
    result = getBikePoints()
    return result

@app.route('/Bike/getBikePointById', methods=['GET'])
def getBikePointsById():
    id = request.args.get('id', default = None, type = str)
    if type(id) is not str:
        return Response("The given id must be of type string", 422)
    result = getBikePointById(id)
    return result

@app.route('/Bike/getBikePointByQuery', methods=['GET'])
def getBikePointsByQuery():
    query = request.args.get('query', default = None, type = str)
    if type(query) is not str:
        return Response("The query must be of type string", 422)
    result = getBikePointByQuery(query)
    return result

@app.route('/Occupancy/getCarParkById', methods=['GET'])
def getCarParkById():
    id = request.args.get('id', default = None, type = str)
    if type(id) is not str:
        return Response("The query must be of type string", 422)
    result = getCarParkOccupancyById(id)
    return result

@app.route('/Occupancy/getChargeById', methods=['GET'])
def getChargeById():
    id = request.args.get('id', default = None, type = str)
    if type(id) is not str:
        return Response("The query must be of type string", 422)
    result = getChargeConnectorById(id)
    return result

@app.route('/Occupancy/getBikePointById', methods=['GET'])
def getConnectorById():
    id = request.args.get('id', default = None, type = str)
    if type(id) is not str:
        return Response("The query must be of type string", 422)
    result = getBikePointOccupancyById(id)
    return result

@app.route('/Place/GetPlaceByTypeAndStatus', methods=['GET'])
def getPlaceByTypeAndStatus():
    placeType = request.args.get('type', default = None, type = str)
    placeStatus = request.args.get('status', default = None, type = str)
    if type(placeType) is not str or type(placeStatus) is not str:
        return Response("The query must be of type string", 422)
    result = getPlacesByTypeAndStatus(placeType, placeStatus)
    return result

@app.route('/Place/GetPlaceById', methods=['GET'])
def getPlacesById():
    id = request.args.get('id', default = None, type = str)
    if type(id) is not str:
        return Response("The query must be of type string", 422)
    result = getPlaceById(id, True)
    return result

@app.route('/Place/GetPlaceByBounds', methods=['GET'])
def getPlacesByBounds():
    placeType = request.args.get('type', default = None, type = str)
    lat = request.args.get('Lat', default = None, type = str)
    lon = request.args.get('Lon', default = None, type = str)
    if type(placeType) is not str or type(lat) is not str or type(lon) is not str:
        return Response("The query must be of type string", 422)
    result = getPlaceAtLongAndLat(placeType, lat, lon, lat, lon)
    return result

@app.route('/Place/GetPlaceByName', methods=['GET'])
def getPlacesByName():
    name = request.args.get('name', default = None, type = str)
    placeType = request.args.get('type', default = None, type = str)
    if type(name) is not str or type(placeType) is not str:
        return Response("The query must be of type string", 422)
    result = getPlaceByName(name, placeType)
    return result

@app.route('/StopPoint/GetStopPointById', methods=['GET'])
def getStopPointInfoById():
    id = request.args.get('id', default = None, type = str)
    crowded = request.args.get('isCrowded', default = "true", type = str)
    if type(id) is not str:
        return Response("The query must be of type string", 422)
    result = getStopPointById(id, crowded)
    return result

@app.route('/StopPoint/GetStopPointByIdAndType', methods=['GET'])
def getStopPointInfoByIdAndType():
    id = request.args.get('id', default = None, type = str)
    placeType = request.args.get('type', default = None, type = str)
    if type(id) is not str or type(placeType) is not str:
        return Response("The query must be of type string", 422)
    result = getStopPointByIdAndType(id, placeType)
    return result

@app.route('/StopPoint/GetCrowdingByStopLineDirection', methods=['GET'])
def getCrowdingByStopLineDirection():
    stopid = request.args.get('stopid', default = None, type = str)
    lineid = request.args.get('lineid', default = None, type = str)
    direction = request.args.get('direction', default = None, type = str)
    direction = direction.lower()
    lineid = lineid.lower()
    if type(stopid) is not str or type(lineid) is not str or (direction != "outbound" and direction != "inbound"):
        return Response("The query must be of type string", 422)
    result = getCrowdingByIdAndLineAndDirection(stopid, lineid, direction)
    return result

@app.route('/StopPoint/GetStopByType', methods=['GET'])
def getStopByType():
    stopType = request.args.get('type', default = None, type = str)
    if type(stopType) is not str:
        return Response("The query must be of type string", 422)
    result = getStopsOfType(stopType)
    return result

@app.route('/StopPoint/GetServicesForStop', methods=['GET'])
def getServicesForStopPoint():
    stopid = request.args.get('stopid', default = None, type = str)
    lineid = request.args.get('lineid', default = None, type = str)
    mode = request.args.get('mode', default = None, type = str)
    if type(stopid) is not str:
        return Response("The query must be of type string", 422)
    result = getServicesForStop(stopid, lineid, mode)
    return result

@app.route('/StopPoint/GetArrivalsForStop', methods=['GET'])
def getArrivalsForStopPoint():
    stopid = request.args.get('stopid', default = None, type = str)
    if type(stopid) is not str:
        return Response("The query must be of type string", 422)
    result = getArrivalsByStopId(stopid)
    return result

@app.route('/StopPoint/GetStopsOnLineFromStop', methods=['GET'])
def getStopsOnLineFromStop():
    stopid = request.args.get('stopid', default = None, type = str)
    lineid = request.args.get('lineid', default = None, type = str)
    serviceType = request.args.get('servicetype', default = None, type = str)
    if type(stopid) is not str or type(lineid) is not str:
        return Response("The query must be of type string", 422)
    result = getStopsFromStationAndLine(stopid, lineid, serviceType)
    return result

@app.route('/StopPoint/GetRouteSectionsFromStop', methods=['GET'])
def getRouteSectionsfromStop():
    stopid = request.args.get('stopid', default = None, type = str)
    serviceType = request.args.get('servicetype', default = None, type = str)
    if type(stopid) is not str:
        return Response("The query must be of type string", 422)
    result = getRouteSectionsForStopPoint(stopid, serviceType)
    return result

@app.route('/StopPoint/GetDisruptionsForMode', methods=['GET'])
def getDisruptionsOnMode():
    servicemode = request.args.get('mode', default = None, type = str)
    includeblocked = request.args.get('includeblocked', default = "true", type = str)
    if type(servicemode) is not str:
        return Response("The query must be of type string", 422)
    result = getDisruptionsForMode(servicemode, includeblocked)
    return result

@app.route('/StopPoint/GetDisruptionsForStopPoint', methods=['GET'])
def getDisruptionsForStopPoint():
    stopid = request.args.get('stopid', default = None, type = str)
    getfamily = request.args.get('getfamily', default = "false", type = str)
    includeblocked = request.args.get('includeblocked', default = "true", type = str)
    flatten = request.args.get('flatten', default = None, type = str)
    if getfamily is None or getfamily is "false":
        flatten = False
    else:
        flatten = True
    if type(stopid) is not str:
        return Response("The query must be of type string", 422)
    result = getDisruptionsForStop(stopid, getfamily, includeblocked, flatten)
    return result

@app.route('/StopPoint/GetStopsWithinRadius', methods=['GET'])
def getStopsWithinRadius():
    stopType = request.args.get('type', default = None, type = str)
    radius = request.args.get('radius', default = 200, type = str)
    mode = request.args.get('mode', default = None, type = str)
    categories = request.args.get('categories', default = None, type = str)
    includelines = request.args.get('lines', default = "true", type = str)
    lat = request.args.get('lat', default = None, type = str)
    lon = request.args.get('lon', default = None, type = str)
    if type(stopType) is not str or type(lat) is not str or type(lon) is not str:
        return Response("The query must be of type string", 422)
    result = getStopPointsWithinRadius(stopType, radius, mode, categories, includelines, lat, lon)
    return result

@app.route('/StopPoint/GetStopsByMode', methods=['GET'])
def getStopsByMode():
    servicemode = request.args.get('mode', default = None, type = str)
    page = request.args.get('page', default = "1", type = str)
    if page == "":
        page = "1"
    if type(servicemode) is not str:
        return Response("The query must be of type string", 422)
    result = getAllStopsByMode(servicemode, page)
    return result

@app.route('/StopPoint/GetStopPointsByQuery', methods=['GET'])
def getStopsByQuery():
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
        return Response("The query must be of type string", 422)
    result = searchStopPointsByQuery(query, modes, faresOnly, results, lines, includeHubs, tflOnly)
    return result

@app.route('/StopPoint/GetCarParksAtStopPoint', methods=['GET'])
def getCarParksAtStop():
    stopid = request.args.get('stopid', default = None, type = str)
    if type(stopid) is not str:
        return Response("The query must be of type string", 422)
    result = getCarParksAtStopPoint(stopid)
    return result