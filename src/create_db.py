import sqlite3

query = """
BEGIN TRANSACTION;

DROP TABLE IF EXISTS student;
CREATE TABLE student (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));

COMMIT TRANSACTION;
"""


with sqlite3.connect("patterns.sqlite") as db:
    cursor = db.cursor()
    cursor.executescript(query)
    cursor.close()
