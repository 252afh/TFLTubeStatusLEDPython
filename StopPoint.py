import requests
from flask import jsonify, current_app, Response, request
from Settings import Settings
from DatabaseAccess import DatabaseAccess


class StopPoint:

    @staticmethod
    def get_stop_point_by_id(stop_id, is_crowded):
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
            if stop_id is None:
                DatabaseAccess.insert_error('stopId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given stop id was None", 422)
            result_url = '{}StopPoint/{}?{}&{}'.format(Settings.ApiUrl, stop_id, Settings.appid, Settings.appkey)
            if is_crowded is not None:
                result_url += '&includeCrowdingData={}'.format(is_crowded)
            result = requests.get(result_url)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_stop_point_by_id_and_type(stop_id, place_type):
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
            if stop_id is None or place_type is None:
                DatabaseAccess.insert_error('stopId must not be None, value was None. placeType must not be none,'
                                            'value was None.', 422, request.url, request.remote_addr)
                return Response("The given arguments are None", 422)
            result = requests.get('{}StopPoint/{}/placeTypes?placeTypes={}&{}&{}'.format(Settings.ApiUrl, stop_id,
                                                                                         place_type, Settings.appid,
                                                                                         Settings.appkey))
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_crowding_by_id_and_line_and_direction(stop_id, line_id, direction):
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
            if stop_id is None or line_id is None or direction is None:
                DatabaseAccess.insert_error('stopId must not be None, value was None. lineId must not be None,'
                                            'value was None. direction must not be None, value was None.', 422,
                                            request.url, request.remote_addr)
                return Response("The given arguments are None", 422)
            result = requests.get('{}StopPoint/{}/Crowding/{}?direction={}&{}&{}'.format(Settings.ApiUrl, stop_id,
                                                                                         line_id, direction,
                                                                                         Settings.appid,
                                                                                         Settings.appkey))
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_stops_of_type(stop_type):
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
            if stop_type is None:
                DatabaseAccess.insert_error('stopType must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given argument was None", 422)
            result = requests.get('{}StopPoint/Type/{}?{}&{}'.format(Settings.ApiUrl, stop_type, Settings.appid,
                                                                     Settings.appkey))
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_services_for_stop(stop_id, line_id, service_mode):
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
            if stop_id is None:
                DatabaseAccess.insert_error('stopId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given stop id is None", 422)
            result_url = '{}StopPoint/ServiceTypes?id={}&{}&{}'.format(Settings.ApiUrl, stop_id, Settings.appid,
                                                                       Settings.appkey)
            if line_id is not None:
                result_url += '&lineIds={}'.format(line_id)
            if service_mode is not None:
                result_url += '&modes={}'.format(service_mode)
            result = requests.get(result_url)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_arrivals_by_stop_id(stop_id):
        """ Returns arrivals at the given stop point
        Required:
            stopid is a single string representing a station
        Optional:
        Example: 940GZZLUASL
        Note: The URL provided by TFLs swagger file is incorrect
        URL: https://api.tfl.gov.uk/StopPoint/940GZZLUASL/Arrivals?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            if stop_id is None:
                DatabaseAccess.insert_error('stopId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given stop id is None", 422)
            result = requests.get('{}StopPoint/{}/Arrivals?{}&{}'.format(Settings.ApiUrl, stop_id, Settings.appid,
                                                                         Settings.appkey))
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_stops_from_station_and_line(stop_id, line_id, service):
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
            if stop_id is None or line_id is None:
                DatabaseAccess.insert_error('stopId must not be None, value was None. lineId must not be None,'
                                            'value was None.', 422, request.url, request.remote_addr)
                return Response("The given stop or line id was None", 422)
            result_url = '{}StopPoint/{}/CanReachOnLine/{}?{}&{}'.format(Settings.ApiUrl, stop_id, line_id,
                                                                        Settings.appid, Settings.appkey)
            if service is not None:
                result_url += '&serviceTypes={}'.format(service)
            result = requests.get(result_url)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_route_sections_for_stop_point(stop_id, service_type):
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
            if stop_id is None:
                DatabaseAccess.insert_error('stopId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given stop id was None", 422)
            result_url = '{}StopPoint/{}/Route?{}&{}'.format(Settings.ApiUrl, stop_id, Settings.appid, Settings.appkey)
            if service_type is not None:
                result_url += '&serviceTypes={}'.format(service_type)
            result = requests.get(result_url)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_disruptions_for_mode(mode, include_blocked):
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
                DatabaseAccess.insert_error('mode must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given mode was None", 422)
            if include_blocked is None:
                include_blocked = True
            result = requests.get('{}StopPoint/Mode/{}/Disruption?includeRouteBlockedStops={}&{}&{}'
                                  .format(Settings.ApiUrl, mode, include_blocked, Settings.appid, Settings.appkey))
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_disruptions_for_stop(stop_id, get_family, include_route_blocked, flatten_response):
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
            if stop_id is None:
                DatabaseAccess.insert_error('stopId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return "The given stop id was None", 422
            if get_family is None:
                get_family = False
            if flatten_response is True and get_family is not True:
                flatten_response = False
            result_url = '{}StopPoint/{}/Disruption?{}&{}'.format(Settings.ApiUrl, stop_id, Settings.appid,
                                                                 Settings.appkey)
            if get_family is not None:
                result_url += '&getFamily={}'.format(get_family)
            if include_route_blocked is not None:
                result_url += '&includeRouteBlockedStops={}'.format(include_route_blocked)
            if flatten_response is not None:
                result_url += '&flattenResponse={}'.format(flatten_response)
            result = requests.get(result_url)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_stop_points_within_radius(stop_type, radius, modes, categories, get_lines, lat, lon):
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
            if stop_type is None or lat is None or lon is None:
                DatabaseAccess.insert_error('stopType must not be None, value was None. lat must not be None,'
                                            'value was None. lon must not be None, value was None.', 422, request.url,
                                            request.remote_addr)
                return Response("The given arguments are None", 422)
            if categories is None:
                categories = "none"
            if radius is None:
                radius = 200
            result_url = '{}StopPoint?stopTypes={}&radius={}&useStopPointHierarchy=true&categories={}&returnLines={}&' \
                        'lat={}&lon={}&{}&{}'.format(Settings.ApiUrl, stop_type, radius, categories, get_lines, lat,
                                                     lon, Settings.appid, Settings.appkey)
            if modes is not None:
                result_url += '&modes={}'.format(modes)
            result = requests.get(result_url)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_all_stops_by_mode(mode, page):
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
                DatabaseAccess.insert_error('mode must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given mode was None", 422)
            if page is None:
                page = 1
            result = requests.get('{}StopPoint/Mode/{}?page={}&{}&{}'.format(Settings.ApiUrl, mode, page,
                                                                             Settings.appid, Settings.appkey))
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def search_stop_points_by_query(query_string, modes, fares_only, max_results, lines, include_hubs, tfl_only):
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
            if query_string is None:
                DatabaseAccess.insert_error('queryString must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given query string was None", 422)
            if fares_only is None:
                fares_only = False
            if max_results is None:
                max_results = 1
            if include_hubs is None:
                include_hubs = True
            if tfl_only is None:
                tfl_only = False
            result_url = '{}StopPoint/Search?query={}&faresOnly={}&maxResults={}&includeHubs={}&' \
                        'tflOperatedNationalRailStationsOnly={}&{}&{}'.format(Settings.ApiUrl, query_string, fares_only,
                                                                              max_results, include_hubs, tfl_only,
                                                                              Settings.appid, Settings.appkey)
            if modes is not None:
                result_url += '&modes={}'.format(modes)
            if lines is not None:
                result_url += '&lines={}'.format(lines)
            result = requests.get(result_url)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_car_parks_at_stop_point(stop_id):
        """ Returns information regarding car parks at a stop point
        Required:
            stopid cannot be an array, must be a single string corresponding to a station Id
        Example: 940GZZLUWYP
        Note: The given URL on the TFL swagger API file is incorrect
        URL: https://api.tfl.gov.uk/StopPoint/940GZZLUWYP/CarParks?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            if stop_id is None:
                DatabaseAccess.insert_error('stopId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given stop id was None", 422)
            result = requests.get('{}StopPoint/{}/CarParks?{}&{}'.format(Settings.ApiUrl, stop_id, Settings.appid,
                                                                         Settings.appkey))
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)