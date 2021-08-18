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


def insert_data_books():

    con = create_connection("database\libscout.db")
    cur = con.cursor()
    file = open("db.json")
    books = json.load(file)["books"]
    for book in books:
        cur.execute(
            'INSERT INTO BOOKS VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(
                bytes(book["category"], "utf-8").decode("unicode_escape"),
                bytes(book["current_category"], "utf-8").decode("unicode_escape"),
                bytes(book["id"], "utf-8").decode("unicode_escape"),
                bytes(book["lib_id"], "utf-8").decode("unicode_escape"),
                bytes(book["author"], "utf-8").decode("unicode_escape"),
                str(bytes(book["title"], "utf-8").decode("unicode_escape")).split(' / ')[0],
                book["status"],
            )
        )
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


def get_ordered_books():
    con = create_connection("database\libscout.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM BOOKS ORDER BY category, CAST(lib_id AS DECIMAL);")
    books = cur.fetchall()
    con.commit()
    con.close()
    return books
    

def update_book(current_category, status, id):

    con = create_connection("database\libscout.db")
    cur = con.cursor()
    
    cur.execute(
            'UPDATE BOOKS SET \
                            current_category = "{}", \
                            status = "{}" \
            WHERE id = "{}";'.format(current_category, status, id)
        )
        
    con.commit()
    con.close()
