import os

import psycopg2

from dotenv import load_dotenv

load_dotenv()


DATABASE = os.environ.get("DATABASE")
USER = os.environ.get("USER")
HOST = os.environ.get("HOST")
PASSWORD = os.environ.get("PASSWORD")
PORT = os.environ.get("PORT")


def connect():
    try:

        conn = psycopg2.connect(
            database="wot",
            user="manager",
            host="localhost",
            password="123",
            port="5452",
        )

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)

    return conn


def create_table(statement):
    """
    "CREATE TABLE pages (
        id INT PRIMARY KEY,
        page_id INT,
        title VARCHAR(50),
        content TEXT,
        sections jsonb)"
    """
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute(statement)

    except:

        print("error")

    conn.commit()


def insert_page(page_id, title, content, sections):

    conn = connect()
    cursor = conn.cursor()

    statement = (
        "INSERT INTO pages (page_id, title, content, sections) VALUES (%s, %s, %s, %s);"
    )
    data = (page_id, title, content, sections)

    try:
        cursor.execute(statement, data)

    except Exception as e:

        print(e)

    conn.commit()
