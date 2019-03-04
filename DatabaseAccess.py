import mysql.connector as mariadb
from datetime import datetime

mariadb_connection = mariadb.connect(user='EMoore', password='Pa$$w0rd', database='FlaskAPIRequests')
cursor = mariadb_connection.cursor()

def InsertRequest(url, method, requestOrigin, responseData):
    statement = "INSERT INTO Request (CalledUrl, Method, Origin, ResponseData, CalledDate) values (%s, %s, %s, %s, %s)"
    cursor.execute(statement, (url, method, requestOrigin, responseData, datetime.now()))
    mariadb_connection.commit()

def InsertError(errorMessage, errorCode, url, origin):
    statement = "INSERT INTO Errors (ErrorMessage, ErrorCode, CalledUrl, Origin, CalledDate) values (%s, %s, %s, %s, %s)"
    cursor.execute(statement, (errorMessage, errorCode, url, origin, datetime.now()))
    mariadb_connection.commit()

def test():
    cursor.execute("SELECT ResponseData from Request")
    for ResponseData in cursor:
        print('Response Data: {}'.format(ResponseData))