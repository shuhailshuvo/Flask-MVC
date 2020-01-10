import mysql.connector
from mysql.connector import Error

def connect():
    connection = mysql.connector.connect(host='localhost', database='pydb', user='root', password='')
    return connection
