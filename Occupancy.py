import requests
from flask import jsonify, current_app, Response, request
from Settings import Settings
from DatabaseAccess import DatabaseAccess


class Occupancy:

    @staticmethod
    def get_car_park_occupancy_by_id(car_park_id):
        """ Returns occupancy of a car park based on the id
        Required:
            id is a single string for the car park id to search for
        Optional:
        Example: CarParks_800477
        Note: The URL given by the TFL documentation does not work
        URL: https://api.tfl.gov.uk/Occupancy/CarPark/CarParks_800491?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            if car_park_id is None:
                DatabaseAccess.insert_error('carParkId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given car park id was empty", 422)
            result = requests.get('{}Occupancy/CarPark/{}?{}&{}'.format(Settings.ApiUrl, car_park_id, Settings.appid,
                                                                        Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}'.format(result.status_code), result.status_code, request.url,
                                            request.remote_addr)
                return None
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_car_park_occupancy():
        """ Returns occupancy of all car parks
        Required:
            id is a single string for the car park id to search for
        Optional:
        Example: CarParks_800477
        Note: The URL given by the TFL documentation does not work
        URL: https://api.tfl.gov.uk/Occupancy/CarPark?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            result = requests.get(
                '{}Occupancy/CarPark/?{}&{}'.format(Settings.ApiUrl, Settings.appid, Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}'.format(result.status_code), result.status_code, request.url,
                                            request.remote_addr)
                return None
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_charge_connector_by_id(connector_id):
        """ Returns occupancy of a charge point based on the id
        Required:
            id is an array or single string for the charge point id to search for
        Optional:
        Example: ChargePointESB-UT092S-1
        Note: The URL given by the TFL documentation does not work
        URL: https://api.tfl.gov.uk/Occupancy/ChargeConnector/ChargePointESB-UT092S-1?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            if connector_id is None:
                DatabaseAccess.insert_error('connectorId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given charge connector id was empty", 422)
            result = requests.get('{}Occupancy/ChargeConnector/{}?{}&{}'.format(Settings.ApiUrl, connector_id,
                                                                                Settings.appid, Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}'.format(result.status_code), result.status_code, request.url,
                                            request.remote_addr)
                return None
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_all_charge_point_occupancy():
        """ Returns occupancy of all charge points
        Required:
        Optional:
        Example:
        Note: The URL given by the TFL documentation does not work
        URL: https://api.tfl.gov.uk/Occupancy/ChargeConnector/?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """
        with current_app.app_context():
            result = requests.get('{}Occupancy/ChargeConnector/?{}&{}'.format(Settings.ApiUrl, Settings.appid,
                                                                              Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}'.format(result.status_code), result.status_code, request.url,
                                            request.remote_addr)
                return None
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)

    @staticmethod
    def get_bike_point_occupancy_by_id(bike_point_id):
        """ Returns occupancy of a bike point based on the id
        Required:
            id is the bike point id to search for
        Optional:
        Example: BikePoints_1
        Note: The URL given by the TFL documentation does not work
        URL:https://api.tfl.gov.uk/Occupancy/BikePoints/BikePoints_1?app_id=d83cbf0b&app_key=486727de8027a1be9a212c5d5c2ae8df
        """

        with current_app.app_context():
            if bike_point_id is None:
                DatabaseAccess.insert_error('bikePointId must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("The given bike point id is empty", 422)
            result = requests.get('{}Occupancy/BikePoints/{}?{}&{}'.format(Settings.ApiUrl, bike_point_id,
                                                                           Settings.appid, Settings.appkey))
            if result.status_code != 200:
                DatabaseAccess.insert_error('status code was {}'.format(result.status_code), result.status_code, request.url,
                                            request.remote_addr)
                return None
            if result is None or result == []:
                DatabaseAccess.insert_error('result must not be None, value was None', 422, request.url,
                                            request.remote_addr)
                return Response("No result could be found", 422)
            return jsonify(result.text)