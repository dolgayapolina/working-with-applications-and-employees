import psycopg2


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="polina",
        password=""
    )


def get_cursor(connection):
    return connection.cursor()


def close_connection(connection):
    if connection:
        connection.close()
