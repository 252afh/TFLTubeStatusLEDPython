import datetime
import dateutil.relativedelta
from Settings import Settings


class DatabaseAccess:

    @staticmethod
    def insert_request(url, method, requestOrigin, responseData):
        statement = "INSERT INTO Request (CalledUrl, Method, Origin, ResponseData, CalledDate) values (%s, %s, %s, %s, %s)"
        Settings.cursor.execute(statement, (url, method, requestOrigin, responseData, datetime.now()))
        Settings.mariadb_connection.commit()

    @staticmethod
    def insert_error(errorMessage, errorCode, url, origin):
        statement = "INSERT INTO Errors (ErrorMessage, ErrorCode, CalledUrl, Origin, CalledDate) values (%s, %s, %s, %s, %s)"
        Settings.cursor.execute(statement, (errorMessage, errorCode, url, origin, datetime.now()))
        Settings.mariadb_connection.commit()

    @staticmethod
    def get_top_three_origins():
        statement = "SELECT Origin, COUNT(Origin) AS value_occurrence FROM Request GROUP BY Origin ORDER BY value_occurrence DESC LIMIT 3;"
        Settings.cursor.execute(statement)
        return Settings.cursor.fetchall()

    @staticmethod
    def get_error_count():
        statement = "SELECT COUNT(*) FROM Errors"
        Settings.cursor.execute(statement)
        return Settings.cursor.fetchone()

    @staticmethod
    def get_success_count():
        statement = "SELECT COUNT(*) FROM Request"
        Settings.cursor.execute(statement)
        return Settings.cursor.fetchone()

    @staticmethod
    def get_last_errors():
        statement = "SELECT * FROM Errors"
        Settings.cursor.execute(statement)
        return Settings.cursor.fetchall()

    @staticmethod
    def get_top_5_urls():
        statement = "SELECT CalledUrl, COUNT(CalledUrl) as urlFrequency FROM Request GROUP BY CalledUrl ORDER BY urlFrequency DESC LIMIT 5"
        Settings.cursor.execute(statement)
        return Settings.cursor.fetchall()

    @staticmethod
    def get_call_dates():
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
