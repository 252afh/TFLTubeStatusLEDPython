import requests
from flask import jsonify, current_app, Response, request
from Settings import Settings
from DatabaseAccess import DatabaseAccess


class BikePoint:

    @staticmethod
    def get_bike_points():
        """ Returns information about all bike points
        Required:
        Optional:
        Example:
        Note: The URL given by the TFL documentation does not work
        URL: https://api.tfl.gov.uk/BikePoint?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            result = requests.get('{}BikePoint?{}&{}'.format(Settings.ApiUrl, Settings.appid, Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}'.format(result.status_code), result.status_code, request.url,
                                            request.remote_addr)
                return None
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_bike_point_by_id(bike_point_id):
        """ Returns information about a bike point based on the id
        Required:
            id is a single string representing the bikepoints id
        Optional:
        Example: BikePoints_1
        Note: The URL given by the TFL documentation does not work
        URL: https://api.tfl.gov.uk/BikePoint/BikePoints_1?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            if bike_point_id is None:
                DatabaseAccess.insert_error('id must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No Bike Point id supplied", 422)
            result = requests.get('{}BikePoint/{}?{}&{}'.format(Settings.ApiUrl, bike_point_id, Settings.appid,
                                                                Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}'.format(result.status_code), result.status_code, request.url,
                                            request.remote_addr)
                return None
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)

    @staticmethod
    def get_bike_point_by_query(search_term):
        """ Returns information about a bike point based on the search query
        Required:
            query is a single string representing the search term
        Optional:
        Example: St. James
        Note: The URL given by the TFL documentation does not work
        URL: https://api.tfl.gov.uk/BikePoint/Search?query=St.%20James&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            if search_term is None:
                DatabaseAccess.insert_error('search_term must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No search term supplied", 422)
            result = requests.get('{}BikePoint/Search?query={}&{}&{}'.format(Settings.ApiUrl, search_term,
                                                                             Settings.appid, Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}'.format(result.status_code), result.status_code, request.url,
                                            request.remote_addr)
                return None
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            text = result.text
            return jsonify(text)
