import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()


def run_script_sql(script):
    with open(script) as f:
        query = f.read()
    c.executescript(query)


run_script_sql('categories.sql')
run_script_sql('clothes.sql')

conn.commit()

conn.close()
