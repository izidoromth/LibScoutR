import sqlite3
from sqlite3 import Error
import json

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    con = None
    try:
        con = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        return con

def execute_query(query):
    con = create_connection("database\libscout.db")
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    con.close()

def insert_data_books():

    con = create_connection("database\libscout.db")
    cur = con.cursor()
    file = open('db.json')
    books = json.load(file)['books']
    for book in books:
        cur.execute("INSERT INTO BOOKS VALUES ('{}', '{}', '{}', '{}', '{}')"
                    .format(book['category'], book['id'], book['libId'], book['author'], book['title']))
    con.commit()
    con.close()

def insert_data_originals():

    con = create_connection("database\libscout.db")
    cur = con.cursor()
    file = open('db.json')
    books = json.load(file)['books']
    for book in books:
        cur.execute("INSERT INTO ORIGINAL_BOOKS VALUES ('{}', '{}', '{}', '{}', '{}')"
                    .format(book['category'], book['id'], book['libId'], book['author'], book['title']))
    con.commit()
    con.close()

def get_books():
    con = create_connection("database\libscout.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM BOOKS")
    books = cur.fetchall()
    con.commit()
    con.close()
    return books

def get_original_books():
    con = create_connection("database\libscout.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM ORIGINAL_BOOKS")
    original_books = cur.fetchall()
    con.commit()
    con.close()
    return original_books

def update_books(books):
    
    con = create_connection("database\libscout.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    for book in books:
        cur.execute("UPDATE ORIGINAL_BOOKS \
                    SET category = '{0}', id = '{1}', libId = '{2}', author = '{3}', title = '{4}'\
                    WHERE id = '{1}'"
                    .format(book['category'], book['id'], book['libId'], book['author'], book['title']))

    cur.execute("SELECT * FROM BOOKS")
    my_books = cur.fetchall()
    con.commit()
    con.close()

    return my_books