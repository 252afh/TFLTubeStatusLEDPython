import requests
from flask import Flask, jsonify, current_app, Response
from Settings import ApiUrl, appid, appkey

def getLineStatus():
    """ Returns a list of all tube and dlr lines and their statuses
    Required:
    Optional:
    Example:
    Note: The URL given by the TFL documentation does not work
    URL: https://api.tfl.gov.uk/Line/Mode/tube%2Cdlr/Status?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        result = requests.get('{}Line/Mode/tube%2Cdlr/Status?{}&{}'.format(ApiUrl, appid, appkey))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getLineById(Id):
    """ Returns a list of lines that match the given line id
    Required:
        id is an array or single string representing the line id to search for
    Optional:
    Example: piccadilly
    Note: The URL given by the TFL documentation does not work
    URL: https://api.tfl.gov.uk/Line/piccadilly?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if Id is None:
            return Response("The supplied Id is empty", 422)
        result = requests.get('{}Line/{}?{}&{}'.format(ApiUrl, Id, appid, appkey))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getLinesByMode(mode):
    """ Returns a list of lines in the given mode
    Required:
        mode is an array or single string representing the given modes lines can runs on
    Optional:
    Example: tube
    Note: The URL given by the TFL documentation does not work
    URL: https://api.tfl.gov.uk/Line/Mode/tube?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if mode is None:
            return Response("The supplied mode is empty", 422)
        result = requests.get('{}Line/Mode/{}?{}&{}'.format(ApiUrl, mode, appid, appkey))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getLineByIdAndService(Id, service):
    """ Returns a list of valid routes for the given lineids and service type
    Required:
        id is an array or single string representing the id of the lines to query
        service is an array or single string representing the type of service to search for
    Optional:
    Example: piccadilly, Regular
    Note: The URL given by the TFL documentation does not work
        If not provided the API defaults to Regular anyway
    URL: https://api.tfl.gov.uk/Line/piccadilly/Route?serviceTypes=Regular&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if Id is None:
            return Response("The supplied Id was empty", 422)
        requestUrl = '{}Line/{}/Route?{}&{}'.format(ApiUrl, Id, appid, appkey)
        if service is not None:
            requestUrl += '&serviceTypes={}'.format(service)
        result = requests.get(requestUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getLineInfoByDateAndId(Id, startDate, endDate, detail):
    """ Returns a list of lines with their status based on the given ids and date range
    Required:
        id is an array or single string representing the id of the lines to query
        start is a single string and is the start date of the query daterange
        end is a single string and is the end date of the query daterange 
    Optional:
    Example: piccadilly, 2018-12-06T13:36:56, 2018-12-09T13:36:56
    Note: The URL given by the TFL documentation does not work
        The 'true' parameter is always true as I always want a detailed return statement 
    URL: https://api.tfl.gov.uk/Line/piccadilly/Status/2018-12-06T13:36:56/to/2018-12-09T13:36:56?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if id is None:
            return Response("The supplied Id was empty", 422)
        if startDate is None:
            return Response("The supplied start date was empty", 422)
        if endDate is None:
            return Response("The supplied end date was empty", 422)
        requestUrl = '{}Line/{}/Status/{}/to/{}?{}&{}'.format(ApiUrl, Id, startDate, endDate, appid, appkey)
        if detail is not None:
            requestUrl += '&detail={}'.format(detail)
        result = requests.get(requestUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getLineStatusbyId(Id, detail):
    """ Returns a list of lines with their status based on the given ids
    Required:
        id is an array or single string representing the id of the lines to query
    Optional:
    Example: piccadilly
    Note: The URL given by the TFL documentation does not work
        The 'true' parameter is always true as I always want a detailed return statement 
    URL: https://api.tfl.gov.uk/Line/piccadilly/Status?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if Id is None:
            return Response("The supplied Id was empty", 422)
        requestUrl = '{}Line/{}/Status?{}&{}'.format(ApiUrl, Id, appid, appkey)
        if detail is not None:
            requestUrl += '&detail={}'.format(detail)
        result = requests.get(requestUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getLinesBySeverityCode(severitycode):
    """ Returns a list of all lines matching the given severity code
    Required:
        severity is a single string between 0 and 14, inclusive, representing the severity on that line 
    Optional:
    Example: 9
    Note: The URL given by the TFL documentation does not work
    URL: https://api.tfl.gov.uk/Line/Status/9?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if severitycode is None:
            return Response("The supplied severity was empty", 422)
        result = requests.get('{}Line/Status/{}?{}&{}'.format(ApiUrl, severitycode, appid, appkey))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getLineStatusByMode(mode, detail):
    """ Returns a list of all line statuses based on the mode
    Required:
        mode is an array or a single string representing the mode(s) to get results for
    Optional:
    Example: tube, true
    Note: The URL given by the TFL documentation does not work
        The 'true' string within the api call is to always include detail within the response
    URL: https://api.tfl.gov.uk/Line/Mode/tube/Status?detail=true&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if mode is None:
            return Response("The supplied line was empty", 422)
        requestUrl = '{}Line/Mode/{mode}/Status?{}&{}'.format(ApiUrl, mode, appid, appkey)
        if detail is not None:
            requestUrl += '&detail={}'.format(detail)
        result = requests.get(requestUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getStationsOnLine(Id, tflOnly):
    """ Returns a list of stations that serve the given line id
    Required:
        lineid is a single string representing the line to get stations on
    Optional:
    Example: piccadilly, true
    Note: The URL given by the TFL documentation does not work
        The 'true' string within the api call is to filter out any non-tfl stations
    URL: https://api.tfl.gov.uk/Line/piccadilly/StopPoints?tflOperatedNationalRailStationsOnly=false&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if Id is None:
            return Response("The supplied Id was empty", 422)
        requestUrl = '{}Line/{}/StopPoints?{}&{}'.format(ApiUrl, Id, appid, appkey)
        if tflOnly is not None:
            requestUrl += '&tflOperatedNationalRailStationsOnly={}'.format(tflOnly)
        result = requests.get(requestUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getTimetableForStationOnLine(stationId, lineId):
    """ Returns a timetable for a journey based on source station id, destination station id and the line id
    Required:
        sourceid is a single string representing the source station id
        destid is a single string representing the destination station id  
        lineid is a single string representing the line to get a timetable for
    Optional:
    Example: 940GZZLUASL, piccadilly
    Note: The URL given by the TFL documentation does not work
    URL: https://api.tfl.gov.uk/Line/piccadilly/Timetable/940GZZLUASL?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if stationId is None:
            return Response("The given station id was empty", 422)
        if lineId is None:
            return Response("The given line id is empty", 422)
        result = requests.get('{}Line/{}/Timetable/{}?{}&{}'.format(ApiUrl, lineId, stationId, appid, appkey))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getTimetableForJourney(sourceId, destId, lineId):
    """ Returns a timetable for a journey based on source station id, destination station id and the line id
    Required:
        sourceid is a single string representing the source station id
        destid is a single string representing the destination station id  
        lineid is a single string representing the line to get a timetable for
    Optional:
    Example: 940GZZLUASL, 940GZZLUASG, piccadilly
    Note: The URL given by the TFL documentation does not work
    URL: https://api.tfl.gov.uk/Line/piccadilly/Timetable/940GZZLUASL/to/940GZZLUASG?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if sourceId is None:
            return Response("The given source station id is empty", 422)
        if destId is None:
            return Response("The given destination station id is empty", 422)
        if lineId is None:
            return Response("The given line id is empty", 422)
        result = requests.get('{}Line/{}/Timetable/{}/to/{}?{}&{}'.format(ApiUrl, lineId, sourceId, destId, appid, appkey))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getDisruptionsForGivenLine(lineId):
    """ Returns information about arrival predictions based on a line id
    Required:
        lineid is an array or single string representing the line to get disruptions for
    Optional:
    Example: waterloo
    Note: The URL given by the TFL documentation does not work
    URL: https://api.tfl.gov.uk/Line/piccadilly/Disruption?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if lineId is None:
            return Response("The given line id was empty", 422)
        result = requests.get('{}Line/{}/Disruption?{}&{}'.format(ApiUrl, lineId, appid, appkey))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getDisruptionsForGivenMode(mode):
    """ Returns information about arrival predictions based on a line id and stop id
    Required:
        mode is an array or single string representing the mode of travel
    Optional:
    Example: tube
    Note: The URL given by the TFL documentation does not work
    URL: https://api.tfl.gov.uk/Line/Mode/tube/Disruption?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if mode is None:
            return Response("The given line mode was empty", 422)
        result = requests.get('{}Line/Mode/{}/Disruption?{}&{}'.format(ApiUrl, mode, appid, appkey))
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)

def getArrivalsForLineAndStop(lineId, sourceId, destId, direction):
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
    URL: https://api.tfl.gov.uk/Line/piccadilly/Arrivals/940GZZLUASL?direction=all&destination=940GZZLUASL&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
    """

    with current_app.app_context():
        if lineId is None:
            return Response("The given line id was empty", 422)
        if sourceId is None:
            return Response("The given line id was empty", 422)
        resultUrl = '{}Line/{}/Arrivals/{}?{}&{}'.format(ApiUrl, lineId, sourceId, appid, appkey)
        if direction is not None:
            resultUrl += '&direction={}'.format(direction)
        if destId is not None:
            resultUrl += '&destinationStationId={}'.format(destId)
        result = requests.get(resultUrl)
        if (result is None or result == []):
            return Response("No result could be found", 422)
        text = result.text
        return jsonify(text)