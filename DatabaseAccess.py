import datetime
import dateutil.relativedelta
from Settings import Settings


class DatabaseAccess:

    @staticmethod
    def insert_request(url, method, request_origin, response_data):
        """
        Inserts a received request into the Request table
        :param url: The URL that was called
        :param method: The HTTP method used
        :param request_origin: The originating IP address
        :param response_data: The JSON response
        :return: None
        """
        statement = "INSERT INTO Request (CalledUrl, Method, Origin, ResponseData, CalledDate) values (%s, %s, %s, %s, %s)"
        Settings.cursor.execute(statement, (url, method, request_origin, response_data, datetime.datetime.now()))
        Settings.mariadb_connection.commit()

    @staticmethod
    def insert_error(error_message, error_code, url, origin):
        """
        Inserts an error into the Errors table
        :param error_message: The error message
        :param error_code: The error code
        :param url: The URL that was called
        :param origin: The originating IP address
        :return: None
        """
        statement = "INSERT INTO Errors (ErrorMessage, ErrorCode, CalledUrl, Origin, CalledDate) values (%s, %s, %s, %s, %s)"
        Settings.cursor.execute(statement, (error_message, error_code, url, origin, datetime.datetime.now()))
        Settings.mariadb_connection.commit()

    @staticmethod
    def get_top_three_origins():
        """
        Retrieves the 3 most common originating IP addresses of calls made to the API
        :return: An array containing SQL results
        """
        statement = "SELECT Origin, COUNT(Origin) AS value_occurrence FROM Request GROUP BY Origin ORDER BY value_occurrence DESC LIMIT 3;"
        Settings.cursor.execute(statement)
        return Settings.cursor.fetchall()

    @staticmethod
    def get_error_count():
        """
        Gets the number of rows in the Errors table
        :return: An array with one element that contains the amount of rows
        """
        statement = "SELECT COUNT(*) FROM Errors"
        Settings.cursor.execute(statement)
        return Settings.cursor.fetchone()

    @staticmethod
    def get_success_count():
        """
        Gets the number of rows in the Request table
        :return: An array with one element that contains the amount of rows
        """
        statement = "SELECT COUNT(*) FROM Request"
        Settings.cursor.execute(statement)
        return Settings.cursor.fetchone()

    @staticmethod
    def get_last_errors():
        """
        Retrieves the 5 most recent errors
        :return: An array containing the rows returned by the SQL statement
        """
        statement = "SELECT * FROM Errors ORDER BY CalledDate DESC LIMIT 5"
        Settings.cursor.execute(statement)
        return Settings.cursor.fetchall()

    @staticmethod
    def get_top_5_urls():
        """
        Retrieves the 5 most frequently called URLs
        :return: An array containing the rows returned by the SQL statement
        """
        statement = "SELECT CalledUrl, COUNT(CalledUrl) as urlFrequency FROM Request GROUP BY CalledUrl ORDER BY urlFrequency DESC LIMIT 5"
        Settings.cursor.execute(statement)
        return Settings.cursor.fetchall()

    @staticmethod
    def get_call_dates():
        """
        Gets the frequency of calls made in the last 6 months, not including errors
        :return: An array containing the dates for the last 6 months and the row count in the Request table for each of the months
        """
        today = datetime.datetime.today()
        one_month = today + dateutil.relativedelta.relativedelta(months=-1)
        two_month = today + dateutil.relativedelta.relativedelta(months=-2)
        three_month = today + dateutil.relativedelta.relativedelta(months=-3)
        four_month = today + dateutil.relativedelta.relativedelta(months=-4)
        five_month = today + dateutil.relativedelta.relativedelta(months=-5)

        months = [today, one_month, two_month, three_month, four_month, five_month]

        result = []

        for month in months:
            statement = "SELECT COUNT(CalledDate) FROM Request where CalledDate like \"%{}-{}%\"".format(month.year, str(month.month).zfill(2))
            Settings.cursor.execute(statement)
            response = Settings.cursor.fetchone()[0]
            result.insert(0, [month, response])

        return result
