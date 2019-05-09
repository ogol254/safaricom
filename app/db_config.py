from flask import current_app
from contextlib import closing
import psycopg2
import os


def connection(url):
    con = psycopg2.connect(url)
    return con


def init_db():
    """Set up the database to stode the user data
    """
    db_url = os.getenv('DATABASE_URL')
    conn = connection(db_url)
    with conn as conn, conn.cursor() as cursor:
        with current_app.open_resource('db.sql', mode='r') as sql:
            cursor.execute(sql.read())
        conn.commit()
        return conn


def init_test_db():
    conn = connection(os.getenv('DATABASE_TEST_URL'))
    destroy_db()
    with conn as conn, conn.cursor() as cursor:
        with current_app.open_resource('db.sql', mode='r') as sql:
            cursor.execute(sql.read())
        conn.commit()
        return conn


def destroy_db():
    conn = connection(os.getenv('DATABASE_TEST_URL'))
    curr = conn.cursor()
    blacklist = """DROP TABLE IF EXISTS blacklist CASCADE; """
    users = """DROP TABLE IF EXISTS users CASCADE; """
    queries = [blacklist, users]
    try:
        for query in queries:
            curr.execute(query)
        conn.commit()
    except:
        print("Fail")
