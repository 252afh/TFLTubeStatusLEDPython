import sys
sys.path.append('/home/pi/Documents/FlaskAPI/TFLAPIScripts')

from Line import Line
from BikePoint import BikePoint
from Occupancy import Occupancy
from Place import Place
from StopPoint import StopPoint
from DatabaseAccess import DatabaseAccess
from flask import Flask, request, Response, render_template
from flask_sslify import SSLify
import pygal
import pdb

app = Flask(__name__)
sslify = SSLify(app)


@app.route('/Line/getAllLineStatus', methods=['GET'])
def get_all_line_status():
    """ Returns a list of all tube and dlr lines and their statuses
    Required:
    Optional:
    Example:
    Note: The URL given by the TFL documentation does not work
    """

    result = Line.get_line_status()
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Line/getLinesById', methods=['GET'])
def get_lines_by_id():
    """ Returns a list of lines that match the given line id
    Required:
        id is an array or single string representing the line id to search for
    Optional:
    Example: piccadilly
    Note: The URL given by the TFL documentation does not work
    """

    line_id = request.args.get('id', default=None, type=str)
    if type(line_id) is not str:
        DatabaseAccess.insert_error('id must be string, value was {}'.format(type(line_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The given Id was not a string", 422)
    result = Line.get_line_by_id(line_id)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Line/getByMode', methods=['GET'])
def get_line_by_mode():
    """ Returns a list of lines in the given mode
    Required:
        mode is an array or single string representing the given modes lines can runs on
    Optional:
    Example: tube
    Note: The URL given by the TFL documentation does not work
    """

    mode = request.args.get('mode', default=None, type=str)
    if type(mode) is not str:
        DatabaseAccess.insert_error('mode must be string, value was {}'.format(type(mode)), 422, request.url,
                                    request.remote_addr)
        return Response("The given mode was not a string", 422)
    result = Line.get_lines_by_mode(mode)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Line/getByServiceAndId', methods=['GET'])
def get_line_by_service_and_id():
    """ Returns a list of valid routes for the given lineids and service type
    Required:
        id is an array or single string representing the id of the lines to query
        service is an array or single string representing the type of service to search for
    Optional:
    Example: piccadilly, Regular
    Note: The URL given by the TFL documentation does not work
        If not provided the API defaults to Regular anyway
    """

    service = request.args.get('service', default="Regular", type=str)
    line_id = request.args.get('id', default=None, type=str)

    if service == "":
        service = "Regular"
    if type(line_id) is not str:
        DatabaseAccess.insert_error('id must be string, value was {}'.format(type(line_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The given id was not a string", 422)
    if service is not None and type(service) is not str:
        DatabaseAccess.insert_error('service must be string, value was {}'.format(type(service)), 422, request.url,
                                    request.remote_addr)
        return Response("The given service was not a string", 422)
    result = Line.get_line_by_id_and_service(line_id, service)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Line/getLineByDateAndId', methods=['GET'])
def get_line_by_date_and_id():
    """ Returns a list of lines with their status based on the given ids and date range
    Required:
        id is an array or single string representing the id of the lines to query
        start is a single string and is the start date of the query date range
        end is a single string and is the end date of the query date range
    Optional:
    Example: piccadilly, 2018-12-06T13:36:56, 2018-12-09T13:36:56
    Note: The URL given by the TFL documentation does not work
        The 'true' parameter is always true as I always want a detailed return statement
    """

    line_id = request.args.get('id', default=None, type=str)
    start = request.args.get('start', default=None, type=str)
    end = request.args.get('end', default=None, type=str)
    if type(line_id) is not str or type(start) is not str or type(end) is not str:
        DatabaseAccess.insert_error(
            'id must be string, value was {}. start must be string, value was {}. end must be string, value was {}'
            .format(type(line_id), type(start), type(end)), 422, request.url, request.remote_addr)
        return Response("Parameters must be string", 422)
    result = Line.get_line_info_by_date_and_id(line_id, start, end, "true")
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    pdb.set_trace()
    return Response("Result was None", 422) if result is None else result


@app.route('/Line/getLineStatusById', methods=['GET'])
def get_status_by_id():
    """ Returns a list of lines with their status based on the given ids
    Required:
        id is an array or single string representing the id of the lines to query
    Optional:
    Example: piccadilly
    Note: The URL given by the TFL documentation does not work
        The 'true' parameter is always true as I always want a detailed return statement
    """

    line_id = request.args.get('id', default=None, type=str)
    if type(line_id) is not str:
        DatabaseAccess.insert_error('id must be string, value was {}'.format(type(line_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The id must be of type string", 422)
    result = Line.get_line_status_by_id(line_id, "true")
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Line/getLineBySeverity', methods=['GET'])
def get_line_by_severity():
    """ Returns a list of all lines matching the given severity code
    Required:
        severity is a single string between 0 and 14, inclusive, representing the severity on that line
    Optional:
    Example: 9
    Note: The URL given by the TFL documentation does not work
    """

    severity = request.args.get('severitycode', default=None, type=str)
    if type(severity) is not str:
        DatabaseAccess.insert_error('severity must be string, value was {}'.format(type(severity)), 422, request.url,
                                    request.remote_addr)
        return Response("Severity code must be of type string", 422)
    result = Line.get_lines_by_severity_code(severity)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Line/getLineStatusByMode', methods=['GET'])
def get_line_status_by_modes():
    """ Returns a list of all line statuses based on the mode
    Required:
        mode is an array or a single string representing the mode(s) to get results for
    Optional:
    Example: tube, true
    Note: The URL given by the TFL documentation does not work
        The 'true' string within the api call is to always include detail within the response
    """

    mode = request.args.get('mode', default=None, type=str)
    if type(mode) is not str:
        DatabaseAccess.insert_error('mode must be string, value was {}'.format(type(mode)), 422, request.url,
                                    request.remote_addr)
        return Response("Mode must be of type string", 422)
    result = Line.get_line_status_by_mode(mode, "true")
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Line/getStationsOnLineById', methods=['GET'])
def get_stations_on_line_by_id():
    """ Returns a list of stations that serve the given line id
    Required:
        line id is a single string representing the line to get stations on
    Optional:
    Example: piccadilly, true
    Note: The URL given by the TFL documentation does not work
        The 'false' string within the api call is to not filter out any non-tfl stations
    """

    line_id = request.args.get('id', default=None, type=str)
    if type(line_id) is not str:
        DatabaseAccess.insert_error('id must be string, value was {}'.format(type(line_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The given id must be of type string", 422)
    result = Line.get_stations_on_line(line_id, "false")
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Line/getSequenceOfStopsOnRoute', methods=['GET'])
def get_sequence_of_stops_on_route():
    """ Returns a list of stations on a route
    Required:
        id is a single string representing the line to get stations on
        direction is a single string of inbound or outbound
    Optional:
    serviceTypes is a single string or array specifying either Regular or Night service
    Example: victoria, inbound, Regular
    Note:
    """

    line_id = request.args.get('id', default=None, type=str)
    direction = request.args.get('direction', default="inbound", type=str)
    service_types = request.args.get('servicetype', default="Regular", type=str)

    if type(line_id) is not str:
        DatabaseAccess.insert_error('id must be string, value was {}'.format(type(line_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The given id must be of type string", 422)
    if type(direction) is not str or (direction != "inbound" and direction != "outbound"):
        direction = "inbound"
    if service_types != "Regular" and service_types != "Night":
        service_types = "Regular"
    result = Line.get_sequence_on_route(line_id, direction, service_types, "false")
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Line/getTimetableForStationOnLine', methods=['GET'])
def get_timetable_for_station_on_line_by_station_id_line_id():
    """ Returns a timetable for a journey based on source station id and the line id
    Required:
        stationid is a single string representing the source station id
        lineid is a single string representing the line to get a timetable for
    Optional:
    Example: 940GZZLUASL, piccadilly
    Note: The URL given by the TFL documentation does not work
    """

    stationid = request.args.get('stationid', default=None, type=str)
    lineid = request.args.get('lineid', default=None, type=str)
    if type(stationid) is not str or type(lineid) is not str:
        DatabaseAccess.insert_error(
            'stationid must be string, value was {}. lineid must be string, value was {}'.format(type(stationid),
                                                                                                 type(lineid)), 422,
            request.url, request.remote_addr)
        return Response("The station id and line id must be of type string", 422)
    result = Line.get_timetable_for_station_on_line(stationid, lineid)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Line/getTimetableForJouneyBySourceIdDestIdLineId', methods=['GET'])
def get_timetable_for_jouney_by_source_id_dest_id_line_id():
    """ Returns a timetable for a journey based on source station id, destination station id and the line id
    Required:
        source id is a single string representing the source station id
        destination id is a single string representing the destination station id
        line id is a single string representing the line to get a timetable for
    Optional:
    Example: 940GZZLUASL, 940GZZLUASG, piccadilly
    Note: The URL given by the TFL documentation does not work
    """

    source_id = request.args.get('sourceid', default=None, type=str)
    dest_id = request.args.get('destid', default=None, type=str)
    line_id = request.args.get('lineid', default=None, type=str)
    if type(source_id) is not str or type(dest_id) is not str or type(line_id) is not str:
        DatabaseAccess.insert_error(
            'sourceid must be string, value was {}. destid must be string, value was {}.'
            'lineid must be string, value was {}'
            .format(type(source_id), type(dest_id), type(line_id)), 422, request.url, request.remote_addr)
        return Response("The source id, destination id and line id must be of type string", 422)
    result = Line.get_timetable_for_journey(source_id, dest_id, line_id)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Line/getDisruptionsByLineId', methods=['GET'])
def get_disruptions_by_line_id():
    """ Returns information about arrival predictions based on a line id
    Required:
        line id is an array or single string representing the line to get disruptions for
    Optional:
    Example: waterloo
    Note: The URL given by the TFL documentation does not work
    """

    line_id = request.args.get('lineid', default=None, type=str)
    if type(line_id) is not str:
        DatabaseAccess.insert_error('lineid must be string, value was {}'.format(type(line_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The given line id must be of type string", 422)
    result = Line.get_disruptions_for_given_line(line_id)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Line/getDisruptionsByMode', methods=['GET'])
def get_disruptions_by_mode():
    """ Returns information about arrival predictions based on a given mode
    Required:
        mode is an array or single string representing the mode of travel
    Optional:
    Example: tube
    Note: The URL given by the TFL documentation does not work
    """

    mode = request.args.get('mode', default=None, type=str)
    if type(mode) is not str:
        DatabaseAccess.insert_error('mode must be string, value was {}'.format(type(mode)), 422, request.url,
                                    request.remote_addr)
        return Response("The given mode must be of type string", 422)
    result = Line.get_disruptions_for_given_mode(mode)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Line/getArrivalsForLineAndStop', methods=['GET'])
def get_arrivals_for_line_and_station():
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

    lineid = request.args.get('lineid', default=None, type=str)
    source = request.args.get('source', default=None, type=str)
    dest = request.args.get('dest', default=None, type=str)
    direction = request.args.get('direction', default="all", type=str)
    if type(lineid) is not str or type(source) is not str:
        DatabaseAccess.insert_error(
            'lineid must be string, value was {}. source must be string, value was {}'.format(type(lineid),
                                                                                              type(source)), 422,
            request.url, request.remote_addr)
        return Response("The line id and source id must be of type string", 422)
    if dest == "":
        dest = None
    if direction == "":
        direction = None
    if dest is not None:
        if type(dest) is not str:
            DatabaseAccess.insert_error('dest must be string, value was {}'.format(type(dest)), 422, request.url,
                                        request.remote_addr)
            return Response("The destination if given must be of type string", 422)
    if direction is not None:
        if type(direction) is not str:
            DatabaseAccess.insert_error('direction must be string, value was {}'.format(type(direction)), 422,
                                        request.url, request.remote_addr)
            return Response("The direction if given must be of type string", 422)
        direction = direction.lower()
        if direction != "inbound" and direction != "outbound" and direction != "all":
            DatabaseAccess.insert_error('direction must be inbound, outbound or all, value was {}'.format(direction),
                                        422, request.url, request.remote_addr)
            return Response("The given direction must be: outbound, inbound or all", 422)
    result = Line.get_arrivals_for_line_and_stop(lineid, source, dest, direction)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Bike/getBikePoints', methods=['GET'])
def get_all_bike_points():
    """ Returns information about all bike points
    Required:
    Optional:
    Example:
    Note: The URL given by the TFL documentation does not work
    """

    result = BikePoint.get_bike_points()
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Bike/getBikePointById', methods=['GET'])
def get_bike_points_by_id():
    """ Returns information about a bike point based on the id
    Required:
        id is a single string representing the bikepoints id
    Optional:
    Example: BikePoints_1
    Note: The URL given by the TFL documentation does not work
    """

    bike_point_id = request.args.get('id', default=None, type=str)
    if type(bike_point_id) is not str:
        DatabaseAccess.insert_error('id must be string, value was {}'.format(type(bike_point_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The given id must be of type string", 422)
    result = BikePoint.get_bike_point_by_id(bike_point_id)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Bike/getBikePointByQuery', methods=['GET'])
def get_bike_points_by_query():
    """ Returns information about a bike point based on the search query
    Required:
        query is a single string representing the search term
    Optional:
    Example: St. James
    Note: The URL given by the TFL documentation does not work
    """

    query = request.args.get('query', default=None, type=str)
    if type(query) is not str:
        DatabaseAccess.insert_error('query must be string, value was {}'.format(type(query)), 422, request.url,
                                    request.remote_addr)
        return Response("The query must be of type string", 422)
    result = BikePoint.get_bike_point_by_query(query)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Occupancy/getCarParkById', methods=['GET'])
def get_car_park_by_id():
    """ Returns occupancy of a carpark based on the id
    Required:
        id is a single string for the car park id to search for
    Optional:
    Example: CarParks_800477
    Note: The URL given by the TFL documentation does not work
    """

    car_park_id = request.args.get('id', default=None, type=str)
    if type(car_park_id) is not str:
        DatabaseAccess.insert_error('id must be string, value was {}'.format(type(car_park_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The query must be of type string", 422)
    result = Occupancy.get_car_park_occupancy_by_id(car_park_id)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Occupancy/getCarParks', methods=['GET'])
def get_car_parks():
    """ Returns occupancy of all carparks
    Required:
    Optional:
    Example:
    Note: The URL given by the TFL documentation does not work
    """

    result = Occupancy.get_car_park_occupancy()
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Occupancy/getChargeById', methods=['GET'])
def get_charge_by_id():
    """ Returns occupancy of a charge point based on the id
    Required:
        id is an array or single string for the charge point id to search for
    Optional:
    Example: ChargePointESB-UT092S-1
    Note: The URL given by the TFL documentation does not work
    """

    charge_connector_id = request.args.get('id', default=None, type=str)
    if type(charge_connector_id) is not str:
        DatabaseAccess.insert_error('id must be string, value was {}'
                                    .format(type(charge_connector_id)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = Occupancy.get_charge_connector_by_id(charge_connector_id)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Occupancy/getAllChargeConnectors', methods=['GET'])
def get_all_charge_connectors():
    """ Returns occupancy of all charge points
        Required:
        Optional:
        Example:
        Note: The URL given by the TFL documentation does not work
        """

    result = Occupancy.get_all_charge_point_occupancy()
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Occupancy/getBikePointById', methods=['GET'])
def get_connector_by_id():
    """ Returns occupancy of a bikepoint based on the id
    Required:
        id is an array or single string for the bikepoint id to search for
    Optional:
    Example: BikePoints_1
    Note: The URL given by the TFL documentation does not work
    """

    charge_connector_id = request.args.get('id', default=None, type=str)
    if type(charge_connector_id) is not str:
        DatabaseAccess.insert_error('id must be string, value was {}'
                                    .format(type(charge_connector_id)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = Occupancy.get_bike_point_occupancy_by_id(charge_connector_id)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Place/GetPlaceByTypeAndStatus', methods=['GET'])
def get_place_by_type_and_status():
    """ Returns places that match the type
    Required:
        type is the type of place to return
    Optional:
        activeOnly is a boolean whether to include only active places
    Example: BikePoint, true
    Note: The URL given by the TFL documentation does not work
        activeonly usually returns no results if set to false, not sure if based on closing times
    """

    place_type = request.args.get('type', default=None, type=str)
    active_only = request.args.get('activeonly', default=None, type=str)
    if type(place_type) is not str or type(active_only) is not str:
        DatabaseAccess.insert_error(
            'placeType must be string, value was {}. activeOnly must be string, value was {}'.format(type(place_type),
                                                                                                     type(active_only)),
            422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = Place.get_places_by_type_and_status(place_type, active_only)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Place/GetPlaceById', methods=['GET'])
def get_places_by_id():
    """ Returns places that match the place id
    Required:
        id is a single string representing the id of a place
    Optional:
    Example: BikePoints_1, true
    Note: The URL given by the TFL documentation does not work
        Another parameter 'includechildren' is always true so has been hard coded in
    """

    place_id = request.args.get('id', default=None, type=str)
    if type(place_id) is not str:
        DatabaseAccess.insert_error('id must be string, value was {}'.format(type(place_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The query must be of type string", 422)
    result = Place.get_place_by_id(place_id, "true")
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Place/GetPlaceByBounds', methods=['GET'])
def get_places_by_bounds():
    """ Returns a list of places filtered by name
    Required:
        swlat is the southwest latitude for the bounding box
        swlon is the southwest longitude for the bounding box
        nelat is the northeast latitude for the bounding box
        nelon is the northeast latitude for the bounding box
    Optional:
        type is an array or single string representing the type of place to search for
        categories is an array or single string representing the categories to include
        include children is a boolean whether or not to include children places
        active only is a boolean whether to include only active places in the results
    Example: NaptanMetroStation, AccessPoint, true, true, 51.516292, -0.179902, 51.522968, -0.165912
    Note: The URL given by the TFL documentation does not work
        I do not know how exactly categories work so it is always empty for now
    """

    place_type = request.args.get('type', default=None, type=str)
    categories = request.args.get('categories', default=None, type=str)
    include_children = request.args.get('includechildren', default="true", type=str)
    active_only = request.args.get('activeonly', default="false", type=str)
    south_west_latitude = request.args.get('swlat', default=None, type=str)
    south_west_longitude = request.args.get('swlon', default=None, type=str)
    north_east_latitude = request.args.get('nelat', default=None, type=str)
    north_east_longitude = request.args.get('nelon', default=None, type=str)

    if place_type == "":
        place_type = None
    if categories == "":
        categories = None
    if include_children == "":
        include_children = "true"
    if active_only == "":
        active_only = "false"
    if type(south_west_latitude) is not str \
            or type(south_west_longitude) is not str \
            or type(north_east_latitude) is not str \
            or type(north_east_longitude) is not str:
        DatabaseAccess.insert_error(
            'swlat must be string, value was {}. swlon must be string, value was {}. '
            'nelat must be string, value was {}. nelon must be string, value was {}.'.format(
                type(south_west_latitude), type(south_west_longitude), type(north_east_latitude),
                type(north_east_longitude)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = Place.get_places_by_bounding_box(categories, include_children, place_type, active_only, south_west_latitude,
                                              south_west_longitude, north_east_latitude, north_east_longitude)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Place/GetPlaceByName', methods=['GET'])
def get_places_by_name():
    """ Returns a list of places filtered by name
    Required:
        name is a single string representing the name of a place
    Optional:
        type is an array or single string representing the type of place to search for
    Example: Brent Cross Stn (LUL), CarPark
    Note: The URL given by the TFL documentation does not work
    """

    name = request.args.get('name', default=None, type=str)
    place_type = request.args.get('type', default=None, type=str)

    if place_type == "":
        place_type = None

    if type(name) is not str:
        DatabaseAccess.insert_error('name must be string, value was {}'.format(type(name)), 422, request.url,
                                    request.remote_addr)
        return Response("The query must be of type string", 422)
    result = Place.get_place_by_name(name, place_type)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/StopPoint/GetStopPointById', methods=['GET'])
def get_stop_point_info_by_id():
    """ Returns a list of stop points filtered by station id
    Required:
        id is a single string representing the station to look from
    Optional:
        isCrowded is a boolean whether to include crowding information
    Example: 940GZZLUASL, true
    Note:
    """

    stop_point_id = request.args.get('id', default=None, type=str)
    crowded = request.args.get('isCrowded', default="true", type=str)

    if crowded == "":
        crowded = "true"

    if type(stop_point_id) is not str:
        DatabaseAccess.insert_error('id must be string, value was {}'.format(type(stop_point_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The query must be of type string", 422)
    result = StopPoint.get_stop_point_by_id(stop_point_id, crowded)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/StopPoint/GetStopPointByIdAndType', methods=['GET'])
def get_stop_point_info_by_id_and_type():
    """ Returns a list of stop points filtered by station id and stop point type
    Required:
        stopid is a single string representing the station to look from
        type is an array or single string representing the type of stop point
    Optional:
    Example: 940GZZLUASL, NaptanMetroStation
    Note:
    """

    stop_id = request.args.get('id', default=None, type=str)
    place_type = request.args.get('type', default=None, type=str)
    if type(stop_id) is not str or type(place_type) is not str:
        DatabaseAccess.insert_error(
            'stopid must be string, value was {}. placeType must be a string, value was {}'.format(type(stop_id),
                                                                                                   type(place_type)),
            422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = StopPoint.get_stop_point_by_id_and_type(stop_id, place_type)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/StopPoint/GetCrowdingByStopLineDirection', methods=['GET'])
def get_crowding_by_stop_line_direction():
    """ Returns crowding information based on the stop, line and direction of travel
    Required:
        stopid is a single string representing the station to look from
        lineid is a single string representing the line to check for crowding
    Optional:
        direction is a string, either 'all', 'inbound' or 'outbound' determining the direction of travel
    Example: 940GZZLUASL, piccadilly, all
    Note: direction is needed for the api call, but there is handling here for if it is missing
    """

    stop_id = request.args.get('stopid', default=None, type=str)
    line_id = request.args.get('lineid', default=None, type=str)
    direction = request.args.get('direction', default="all", type=str)

    if direction == "" or (direction.lower() != "inbound" and direction.lower() != "outbound"):
        direction = "all"

    direction = direction.lower()

    if stop_id is None or line_id is None:
        DatabaseAccess.insert_error('lineid must be string, value was {}'.format(type(line_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The query must be of type string", 422)

    result = StopPoint.get_crowding_by_id_and_line_and_direction(stop_id, line_id, direction)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/StopPoint/GetStopByType', methods=['GET'])
def get_stop_by_type():
    """ Returns services available at a stop point
    Required:
        stoptype is an array or single string representing the stop type to filter by
    Optional:
    Example: NaptanMetroStation
    Note: Maximum of 12 types
        NaptanMetroStation is a normal tube station, e.g. angel
    """

    stop_type = request.args.get('type', default=None, type=str)
    if type(stop_type) is not str:
        DatabaseAccess.insert_error('stopType must be string, value was {}'.format(type(stop_type)), 422, request.url,
                                    request.remote_addr)
        return Response("The query must be of type string", 422)
    result = StopPoint.get_stops_of_type(stop_type)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/StopPoint/GetServicesForStop', methods=['GET'])
def get_services_for_stop_point():
    """ Returns services available at a stop point
    Required:
        stopid is a single string representing a station
    Optional:
        lineid is an array or single string to limit results to only services on the specified lines
        mode is an array or single string limiting the results to only those within the given mode
    Example: 940GZZLUASL, piccadilly, tube
    Note: The URL provided by TFLs swagger file is incorrect
    """

    stop_id = request.args.get('stopid', default=None, type=str)
    line_id = request.args.get('lineid', default=None, type=str)
    mode = request.args.get('mode', default=None, type=str)

    if line_id == "":
        line_id = None
    if mode == "":
        mode = None

    if type(stop_id) is not str:
        DatabaseAccess.insert_error('stopid must be string, value was {}'.format(type(stop_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The query must be of type string", 422)
    result = StopPoint.get_services_for_stop(stop_id, line_id, mode)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/StopPoint/GetArrivalsForStop', methods=['GET'])
def get_arrivals_for_stop_point():
    """ Returns arrivals at the given stop point
    Required:
        stopid is a single string representing a station
    Optional:
    Example: 940GZZLUASL
    Note: The URL provided by TFLs swagger file is incorrect
    """

    stop_id = request.args.get('stopid', default=None, type=str)
    if type(stop_id) is not str:
        DatabaseAccess.insert_error('stopid must be string, value was {}'.format(type(stop_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The query must be of type string", 422)
    result = StopPoint.get_arrivals_by_stop_id(stop_id)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/StopPoint/GetStopsOnLineFromStop', methods=['GET'])
def get_stops_on_line_from_stop():
    """ Returns stop points reachable on the given line from the given stop point
    Required:
        stopid is a single string representing a station
        lineid is a single string representing a line
    Optional:
        servicetype is an array or single string for the type of service to return
    Example: 940GZZLUASL, piccadilly,  Regular
    Note: servicetype must be either 'Regular' or 'Night'
    """

    stop_id = request.args.get('stopid', default=None, type=str)
    line_id = request.args.get('lineid', default=None, type=str)
    service_type = request.args.get('servicetype', default="Regular", type=str)

    if service_type == "regular":
        service_type = "Regular"
    if service_type == "night":
        service_type = "Night"

    if service_type == "" or service_type.lower() != "regular" or service_type.lower() != "night":
        service_type = "Regular"

    if type(stop_id) is not str or type(line_id) is not str:
        DatabaseAccess.insert_error('lineid must be string, value was {}'.format(type(line_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The query must be of type string", 422)
    result = StopPoint.get_stops_from_station_and_line(stop_id, line_id, service_type)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/StopPoint/GetRouteSectionsFromStop', methods=['GET'])
def get_route_sections_from_stop():
    """ Returns route sections for a stop point
    Required:
        stopid is a single string representing a station id
    Optional:
        servicetype is an array or single string for the type of service to return
    Example: 940GZZLUASL, Regular
    Note: servicetype must be either 'Regular' or 'Night'
    """

    stop_id = request.args.get('stopid', default=None, type=str)
    service_type = request.args.get('servicetype', default="Regular", type=str)

    if service_type == "" or service_type.lower() != "regular" or service_type.lower() != "night":
        service_type = "Regular"

    if type(stop_id) is not str:
        DatabaseAccess.insert_error('stopid must be string, value was {}'.format(type(stop_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The query must be of type string", 422)
    result = StopPoint.get_route_sections_for_stop_point(stop_id, service_type)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/StopPoint/GetDisruptionsForMode', methods=['GET'])
def get_disruptions_on_mode():
    """ Returns disruption information based on the given mode
    Required:
        mode is an array or single string representing the mode to filter by
    Optional:
        includeblocked is a boolean whether to include blocked routes
    Example: tube, true
    """

    service_mode = request.args.get('mode', default=None, type=str)
    include_blocked = request.args.get('includeblocked', default="true", type=str)

    if include_blocked == "":
        include_blocked = "true"

    if type(service_mode) is not str:
        DatabaseAccess.insert_error('servicemode must be string, value was {}'.format(type(service_mode)), 422,
                                    request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = StopPoint.get_disruptions_for_mode(service_mode, include_blocked)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/StopPoint/GetDisruptionsForStopPoint', methods=['GET'])
def get_disruptions_for_stop_point():
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

    stop_id = request.args.get('stopid', default=None, type=str)
    get_family = request.args.get('getfamily', default="false", type=str)
    include_blocked = request.args.get('includeblocked', default="true", type=str)
    flatten = request.args.get('flatten', default=None, type=str)

    if get_family == "":
        get_family = "false"
    if include_blocked == "":
        include_blocked = "true"
    if get_family is None or get_family is "false":
        flatten = "false"
    else:
        if flatten is "false" or flatten is "":
            flatten = "false"
        else:
            flatten = "true"

    if type(stop_id) is not str:
        DatabaseAccess.insert_error('stopid must be string, value was {}'.format(type(stop_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The query must be of type string", 422)
    result = StopPoint.get_disruptions_for_stop(stop_id, get_family, include_blocked, flatten)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/StopPoint/GetStopsWithinRadius', methods=['GET'])
def get_stops_within_radius():
    """ Returns information regarding stop points within an area
    Required:
        type is an array or single string for the type of stoppoint to filter
    Optional:
        radius is a string setting the distance, default is 200 if not provided
        mode is an array or string for the modes to filter by
        categories is an array or single string for
        lines is a boolean whether to return line information or not
        lat is a string representing the latitude to be the centre point
        lon is a string representing the longitude to be the centre point
    Example: NaptanMetroStation, 400, tube, Toilets, true, 51.21, -0.21
    Note: categories is a very weird key value list, never got it working so it is ignored
    """

    stop_type = request.args.get('type', default=None, type=str)
    radius = request.args.get('radius', default=200, type=str)
    mode = request.args.get('mode', default=None, type=str)
    categories = request.args.get('categories', default=None, type=str)
    include_lines = request.args.get('lines', default="true", type=str)
    lat = request.args.get('lat', default=None, type=str)
    lon = request.args.get('lon', default=None, type=str)

    if radius == "":
        radius = 200
    if mode == "":
        mode = None
    if categories == "":
        categories = None
    if include_lines == "":
        include_lines = "true"

    if type(stop_type) is not str or type(lat) is not str or type(lon) is not str:
        DatabaseAccess.insert_error(
            'stopType must be string, value was {}. lat must be str, value was {}. lon must be str, value was {}.'
            .format(type(stop_type), type(lat), type(lon)), 422, request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = StopPoint.get_stop_points_within_radius(stop_type, radius, mode, categories, include_lines, lat, lon)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/StopPoint/GetStopsByMode', methods=['GET'])
def get_stops_by_mode():
    """ Returns information regarding stop points based on mode
    Required:
        mode is an array or single string to filter by
    Optional:
        page is an integer containing 1000 results per page in sequence, so
            1000 will include results 1-1000 and 2 will include 1001-2000
    Example: tube, 1
    Note: page is required if the mode is set to 'bus'
    """

    service_mode = request.args.get('mode', default=None, type=str)
    page = request.args.get('page', default="1", type=str)

    if page == "" or page is None:
        page = "1"
    print(service_mode)
    if type(service_mode) is not str:
        DatabaseAccess.insert_error('servicemode must be string, value was {}'.format(type(service_mode)), 422,
                                    request.url, request.remote_addr)
        return Response("The query must be of type string", 422)
    result = StopPoint.get_all_stops_by_mode(service_mode, page)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/StopPoint/GetStopPointsByQuery', methods=['GET'])
def get_stops_by_query():
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

    query = request.args.get('query', default=None, type=str)
    modes = request.args.get('mode', default=None, type=str)
    fares_only = request.args.get('faresonly', default="false", type=str)
    results = request.args.get('results', default="50", type=str)
    lines = request.args.get('lines', default=None, type=str)
    include_hubs = request.args.get('includehubs', default="true", type=str)
    tfl_only = request.args.get('tflonly', default="false", type=str)

    if modes == "":
        modes = None
    if fares_only == "":
        fares_only = "false"
    if results == "":
        results = "50"
    if lines == "":
        lines = None
    if include_hubs == "":
        include_hubs = "true"
    if tfl_only == "":
        tfl_only = "false"

    if type(query) is not str:
        DatabaseAccess.insert_error('query must be string, value was {}'.format(type(query)), 422, request.url,
                                    request.remote_addr)
        return Response("The query must be of type string", 422)
    result = StopPoint.search_stop_points_by_query(query, modes, fares_only, results, lines, include_hubs, tfl_only)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/StopPoint/GetCarParksAtStopPoint', methods=['GET'])
def get_car_parks_at_stop():
    """ Returns information regarding car parks at a stop point
    Required:
        stopid cannot be an array, must be a single string corresponding to a station Id
    Example: 940GZZLUWYP
    """

    stop_id = request.args.get('stopid', default=None, type=str)
    if type(stop_id) is not str:
        DatabaseAccess.insert_error('stopid must be string, value was {}'.format(type(stop_id)), 422, request.url,
                                    request.remote_addr)
        return Response("The query must be of type string", 422)
    result = StopPoint.get_car_parks_at_stop_point(stop_id)
    DatabaseAccess.insert_request(request.url, request.method, request.remote_addr, None if result is None else result.json)
    return Response("Result was None", 422) if result is None else result


@app.route('/Diagnostic')
def display_diagnostics():
    """
    Returns a web page rendered to include the diagnostics graphs and value. Uses the Diagnostics.html template found
    in the 'templates' folder
    :return: A rendered template web page
    """
    top3 = DatabaseAccess.get_top_three_origins()
    total = 0
    top3_chart = pygal.Pie()
    top3_chart.title = 'Top 3 origin IP'
    for row in top3:
        total += row[1]
        top3_chart.add(row[0].decode('utf-8'), [row[1]])

    top3_pie_rendered = top3_chart.render_data_uri()

    errors = DatabaseAccess.get_error_count()[0]

    successes = DatabaseAccess.get_success_count()[0]

    dates = DatabaseAccess.get_call_dates()
    date_chart = pygal.Line(x_label_rotation=20)
    date_chart.title = "Traffic for the last 6 months"
    x_labels = []
    values = []
    for date in dates:
        x_labels.append(date[0].strftime("%h-%y"))
        values.append(date[1])

    date_chart.add("Calls", values)
    date_chart.x_labels = x_labels

    date_chart_rendered = date_chart.render_data_uri()

    error_list = DatabaseAccess.get_last_errors()

    top5_urls = DatabaseAccess.get_top_5_urls()

    return render_template("Diagnostics.html", top_three=top3_pie_rendered, error_count=errors, success_count=successes,
                           errors=error_list, calls=date_chart_rendered, topurls=top5_urls)
