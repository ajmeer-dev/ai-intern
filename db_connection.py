import pymysql

def get_db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="karthi12",
        database="projectbackend",
        cursorclass=pymysql.cursors.DictCursor
    )

