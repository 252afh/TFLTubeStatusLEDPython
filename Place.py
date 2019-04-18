import requests
from flask import jsonify, current_app, Response, request
from Settings import Settings
from DatabaseAccess import DatabaseAccess


class Place:

    @staticmethod
    def get_places_by_type_and_status(place_type, active_only):
        """ Returns places that match the type
        Required:
            type is the type of place to return
        Optional:
            activeOnly is a boolean whether to include only active places
        Example: BikePoint, true
        Note: The URL given by the TFL documentation does not work
        URL: https://api.tfl.gov.uk/Place/Type/BikePoint?activeOnly=false&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            if place_type is None:
                DatabaseAccess.insert_error('place_type must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given place type was empty", 422)
            result_url = '{}Place/Type/{}?{}&{}'.format(Settings.ApiUrl, place_type, Settings.appid, Settings.appkey)
            if active_only is not None:
                result_url += '&activeOnly={}'.format(active_only)
            result = requests.get(result_url)
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('response must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_place_by_id(place_id, include_children):
        """ Returns places that match the place id
        Required:
            id is a single string representing the id of a place
        Optional:
        Example: BikePoints_1, true
        Note: The URL given by the TFL documentation does not work
            Another parameter 'includechildren' is always true so has been hard coded in
        URL: https://api.tfl.gov.uk/Place/BikePoints_1?includeChildren=true&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            if place_id is None:
                DatabaseAccess.insert_error('place_id must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given place id was empty", 422)
            result_url = '{}Place/{}?{}&{}'.format(Settings.ApiUrl, place_id, Settings.appid, Settings.appkey)
            if include_children is not None:
                result_url += '&includeChildren={}'.format(include_children)
            result = requests.get(result_url)
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_places_by_bounding_box(category, include_children, place_type, active_only, south_west_latitude,
                                   south_west_longitude, north_east_latitude, north_east_longitude):
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
        URL: https://api.tfl.gov.uk/Place?includeChildren=true&type=NaptanMetroStation&activeOnly=true&swLat=51.516292&swLon=-0.179902&neLat=51.522968&neLon=-0.165912&app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            if south_west_latitude is None or south_west_longitude is None or north_east_latitude is None\
                    or north_east_longitude is None:
                DatabaseAccess.insert_error('location information must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("A given latitude or longitude was empty", 422)
            result_url = '{}Place?swLat={}&swLon={}&neLat={}&neLon={}&{}&{}'.format(Settings.ApiUrl,
                                                                                    south_west_latitude,
                                                                                    south_west_longitude,
                                                                                    north_east_latitude,
                                                                                    north_east_longitude,
                                                                                    Settings.appid, Settings.appkey)
            if category is not None:
                result_url += '&categories={}'.format(category)
            if include_children is not None:
                result_url += '&includeChildren={}'.format(include_children)
            if place_type is not None:
                result_url += '&type={}'.format(place_type)
            if active_only is not None:
                result_url += '&activeOnly={}'.format(active_only)
            print('request url = {}'.format(result_url))
            result = requests.get(result_url)
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_place_by_name(place_name, place_type):
        """ Returns a list of places filtered by name
        Required:
            name is a single string representing the name of a place
        Optional:
            type is an array or single string representing the type of place to search for
        Example: Brent Cross Stn (LUL), CarPark
        Note: The URL given by the TFL documentation does not work
        URL:  https://api.tfl.gov.uk/Place/Search?name=Brent%20Cross%20Stn%20(LUL)&types=CarPark?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """
        with current_app.app_context():
            if place_name is None or place_type is None:
                DatabaseAccess.insert_error('place_type or place_name must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("A given value was None", 422)
            result = requests.get('{}Place/Search?name={}&types={}&{}&{}'.format(Settings.ApiUrl, place_name,
                                                                                 place_type, Settings.appid,
                                                                                 Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}', result.status_code, request.url,
                                            request.remote_addr).format(result.status_code)
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)
