import sqlite3


def run_script_sql(script_list):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    for script in script_list:
        with open(script) as f:
            query = f.read()
        c.executescript(query)
    conn.commit()
