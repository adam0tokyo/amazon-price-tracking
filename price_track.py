from dotenv import load_dotenv, find_dotenv
import os
import re
from send_mail import *
from datetime import datetime
import time
import psycopg2
import psycopg2.extras
from psycopg2 import sql
from bs4 import BeautifulSoup
import requests

load_dotenv(find_dotenv())
my_db = os.getenv("DBURI")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
}


def scrape_site(target_url):
    # TODO clean up logic, account for US amazon, other price locations
    try:
        page = requests.get(target_url, headers=HEADERS)
        soup = BeautifulSoup(page.content, "lxml")
        title = soup.find(id="productTitle").text
        price = soup.find(class_="a-offscreen").text
        print(title)
        print(price)
        time.sleep(1)  # TODO sleep for ~2-3 seconds in production
        if title is None or price is None:
            # TODO logic here for failed price, send the email
            return None
        return [re.sub("[^0-9.]|\.(?=.*\.)", "", price), title.strip()]
    except Exception as error:
        print(error)


try:
    with psycopg2.connect(my_db) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            # Open a cursor to perform database operations
            cur = conn.cursor()

            cur.execute("SELECT * FROM Scrapes WHERE active_search = true")
            records = cur.fetchall()
            for record in records:
                # print(record)

                newPrice = scrape_site(record[11])
                if newPrice:
                    # TODO logic for below target price, or not
                    print(newPrice)
                    cur.execute(
                        sql.SQL(
                            "UPDATE Scrapes SET initial_price = %s, product_name = %s,lowest_date = %s WHERE id=%s"
                        ).format(sql.Identifier("Scrapes")),
                        [newPrice[0], newPrice[1], datetime.utcnow(), record[0]],
                    )
                    send_mail(record[11], record[3], record[2], newPrice[0])

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
