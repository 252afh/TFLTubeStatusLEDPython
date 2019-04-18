import requests
from flask import jsonify, current_app, Response, request
from Settings import Settings
from DatabaseAccess import DatabaseAccess


class Line:

    @staticmethod
    def get_line_status():
        """ Returns a list of all tube and dlr lines and their statuses
        Required:
        Optional:
        Example:
        Note: The URL given by the TFL documentation does not work
        URL: https://api.tfl.gov.uk/Line/Mode/tube%2Cdlr/Status?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            result = requests.get('{}Line/Mode/tube%2Cdlr/Status?{}&{}'
                                  .format(Settings.ApiUrl, Settings.appid, Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_line_by_id(line_id):
        """ Returns a list of lines that match the given line id
        Required:
            id is an array or single string representing the line id to search for
        Optional:
        Example: piccadilly
        Note: The URL given by the TFL documentation does not work
        URL: https://api.tfl.gov.uk/Line/piccadilly?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            if line_id is None:
                DatabaseAccess.insert_error('Id must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The supplied Id is empty", 422)
            result = requests.get('{}Line/{}?{}&{}'.format(Settings.ApiUrl, line_id, Settings.appid, Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_lines_by_mode(mode):
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
                DatabaseAccess.insert_error('mode must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The supplied mode is empty", 422)
            result = requests.get('{}Line/Mode/{}?{}&{}'.format(Settings.ApiUrl, mode, Settings.appid, Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_line_by_id_and_service(line_id, service):
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
            if line_id is None:
                DatabaseAccess.insert_error('Id must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The supplied Id was empty", 422)
            request_url = '{}Line/{}/Route?{}&{}'.format(Settings.ApiUrl, line_id, Settings.appid, Settings.appkey)
            if service is not None:
                request_url += '&serviceTypes={}'.format(service)
            result = requests.get(request_url)
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_line_info_by_date_and_id(line_id, start_date, end_date, detail):
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
                DatabaseAccess.insert_error('id must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The supplied Id was empty", 422)
            if start_date is None:
                DatabaseAccess.insert_error('startDate must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The supplied start date was empty", 422)
            if end_date is None:
                DatabaseAccess.insert_error('endDate must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The supplied end date was empty", 422)
            request_url = '{}Line/{}/Status/{}/to/{}?{}&{}'.format(Settings.ApiUrl, line_id, start_date, end_date,
                                                                   Settings.appid, Settings.appkey)
            if detail is not None:
                request_url += '&detail={}'.format(detail)
            result = requests.get(request_url)
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_line_status_by_id(line_id, detail):
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
            if line_id is None:
                DatabaseAccess.insert_error('Id must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The supplied Id was empty", 422)
            request_url = '{}Line/{}/Status?{}&{}'.format(Settings.ApiUrl, line_id, Settings.appid, Settings.appkey)
            if detail is not None:
                request_url += '&detail={}'.format(detail)
            result = requests.get(request_url)
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_lines_by_severity_code(severity_code):
        """ Returns a list of all lines matching the given severity code
        Required:
            severity is a single string between 0 and 14, inclusive, representing the severity on that line
        Optional:
        Example: 9
        Note: The URL given by the TFL documentation does not work
        URL: https://api.tfl.gov.uk/Line/Status/9?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            if severity_code is None:
                DatabaseAccess.insert_error('severitycode must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The supplied severity was empty", 422)
            result = requests.get('{}Line/Status/{}?{}&{}'.format(Settings.ApiUrl, severity_code, Settings.appid,
                                                                  Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_line_status_by_mode(mode, detail):
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
                DatabaseAccess.insert_error('mode must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The supplied line was empty", 422)
            request_url = '{}Line/Mode/{mode}/Status?{}&{}'.format(Settings.ApiUrl, mode, Settings.appid,
                                                                   Settings.appkey)
            if detail is not None:
                request_url += '&detail={}'.format(detail)
            result = requests.get(request_url)
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_stations_on_line(line_id, tfl_only):
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
            if line_id is None:
                DatabaseAccess.insert_error('Id must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The supplied Id was empty", 422)
            request_url = '{}Line/{}/StopPoints?{}&{}'.format(Settings.ApiUrl, line_id, Settings.appid,
                                                              Settings.appkey)
            if tfl_only is not None:
                request_url += '&tflOperatedNationalRailStationsOnly={}'.format(tfl_only)
            result = requests.get(request_url)
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_sequence_on_route(line_id, direction, types, exclude_crowding):
        """ Returns a list of stations on a route
        Required:
            id is a single string representing the line to get stations on
            direction is a single string of inbound or outbound
        Optional:
            serviceTypes is a single string or array specifying either Regular or Night service
        Example: victoria, inbound, Regular
        Note:
        """

        with current_app.app_context():
            if line_id is None:
                DatabaseAccess.insert_error('Id must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The supplied Id was empty", 422)
            if direction is None:
                DatabaseAccess.insert_error('direction must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The supplied direction was empty", 422)
            request_url = '{}Line/{}/Route/Sequence/{}?serviceTypes={}&excludeCrowding={}&{}&{}'\
                .format(Settings.ApiUrl, line_id, direction, types, exclude_crowding, Settings.appid, Settings.appkey)
            result = requests.get(request_url)
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_timetable_for_station_on_line(station_id, line_id):
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
            if station_id is None:
                DatabaseAccess.insert_error('stationId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given station id was empty", 422)
            if line_id is None:
                DatabaseAccess.insert_error('lineId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given line id is empty", 422)
            result = requests.get('{}Line/{}/Timetable/{}?{}&{}'
                                  .format(Settings.ApiUrl, line_id, station_id, Settings.appid, Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_timetable_for_journey(source_id, destination_id, line_id):
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
            if source_id is None:
                DatabaseAccess.insert_error('sourceId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given source station id is empty", 422)
            if destination_id is None:
                DatabaseAccess.insert_error('destId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given destination station id is empty", 422)
            if line_id is None:
                DatabaseAccess.insert_error('lineId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given line id is empty", 422)
            result = requests.get('{}Line/{}/Timetable/{}/to/{}?{}&{}'
                                  .format(Settings.ApiUrl, line_id, source_id, destination_id, Settings.appid,
                                          Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_disruptions_for_given_line(line_id):
        """ Returns information about arrival predictions based on a line id
        Required:
            lineid is an array or single string representing the line to get disruptions for
        Optional:
        Example: waterloo
        Note: The URL given by the TFL documentation does not work
        URL: https://api.tfl.gov.uk/Line/piccadilly/Disruption?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            if line_id is None:
                DatabaseAccess.insert_error('lineId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given line id was empty", 422)
            result = requests.get('{}Line/{}/Disruption?{}&{}'.format(Settings.ApiUrl, line_id, Settings.appid,
                                                                      Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_disruptions_for_given_mode(mode):
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
                DatabaseAccess.insert_error('mode must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given line mode was empty", 422)
            result = requests.get('{}Line/Mode/{}/Disruption?{}&{}'.format(Settings.ApiUrl, mode, Settings.appid,
                                                                           Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_arrivals_for_line_and_stop(line_id, source_id, destination_id, direction):
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
            if line_id is None:
                DatabaseAccess.insert_error('lineId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given line id was empty", 422)
            if source_id is None:
                DatabaseAccess.insert_error('sourceId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given line id was empty", 422)
            result_url = '{}Line/{}/Arrivals/{}?{}&{}'.format(Settings.ApiUrl, line_id, source_id, Settings.appid,
                                                              Settings.appkey)
            if direction is not None:
                result_url += '&direction={}'.format(direction)
            if destination_id is not None:
                result_url += '&destinationStationId={}'.format(destination_id)
            result = requests.get(result_url)
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)