import mysql.connector

def create_connection():
    return mysql.connector.connect(
        user='Dale1ter',
        password='Thuglife22',
        host='192.168.31.11',
        database='Minecraft'
    )

def close_connection(connection):
    connection.close()

def execute_query(query, params=None):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        try:
            connection.commit()
        except:
            pass
        result = cursor.fetchall()
        close_connection(connection)
        return result
    except Exception as e:
        print(e)
