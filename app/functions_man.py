import sqlite3

conn = sqlite3.connect("database.db")


def database_connection(query, parameters):
    c = conn.cursor()
    result = c.execute(query, parameters)
    return result
