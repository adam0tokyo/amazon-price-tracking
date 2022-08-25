# from email import message
# from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy
import re
import os
from dotenv import load_dotenv, find_dotenv

from datetime import datetime

# from send_mail import send_mail
# import random
import psycopg2
import psycopg2.extras
from psycopg2 import sql

from bs4 import BeautifulSoup
import requests
import time

load_dotenv(find_dotenv())

# my_db_name = os.getenv("MY_DB_NAME")
# my_db_user = os.getenv("MY_DB_USER")
# my_db_pass = os.getenv("MY_DB_PASS")
# my_db_host = os.getenv("MY_DB_HOST")
my_db = os.getenv("DBURI")
# my_db_port = os.getenv("MAILUSERNAME")


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
}


def scrape_site(target_url):
    try:
        page = requests.get(target_url, headers=HEADERS)
        soup = BeautifulSoup(page.content, "lxml")
        title = soup.find(id="productTitle").text
        price = soup.find(class_="a-offscreen").text
        print(title)
        print(price)
        time.sleep(1)
        if title is None or price is None:
            print("something went wrong")
            return None
        # logic for emails?
        return [re.sub("[^0-9.]|\.(?=.*\.)", "", price), title]
    except Exception as error:
        print(error)


try:
    with psycopg2.connect(my_db) as conn:
        #     dbname={my_db_name}, user={my_db_user}, password={my_db_pass}, host={my_db_host}
        # )
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # Open a cursor to perform database operations
            cur = conn.cursor()

            # Execute a query
            cur.execute("SELECT * FROM Scrapes WHERE active_search = false")
            records = cur.fetchall()

            for record in records:
                newPrice = scrape_site(record[3])
                if newPrice:
                    # print(newPrice)
                    cur.execute(
                        sql.SQL(
                            "UPDATE Scrapes SET initial_price = %s, lowest_date = %s WHERE id=%s"
                        ).format(sql.Identifier("Scrapes")),
                        [newPrice[0], datetime.utcnow(), record[0]],
                    )
                    # TODO handle edge cases, other variables, update based on output, test in amazon us
                    # TODO link in send mails
                    # TODO setup basic email, DEPLOY!! <~~tomorrow goal
                # print(type(record[3]), record[3])

            # update_script = 'UPDATE employee SET salary = salary + (salary * 0.5)'
            #         cur.execute(update_script)

            # Retrieve query results
            # print(records)

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
