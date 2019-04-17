import mysql.connector as mariadb


class Settings:
    ApiUrl = "https://api.tfl.gov.uk/"
    appid = "app_id=d83cbf0b"
    appkey = "app_key=486727de8027a1be9a212c5d5c2ae8df"
    mariadb_connection = mariadb.connect(user='EMoore', password='Pa$$w0rd', database='FlaskAPIRequests')
    cursor = mariadb_connection.cursor()
