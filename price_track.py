from dotenv import load_dotenv, find_dotenv
import os
import re
from send_mail import send_mail_found, send_mail_problem
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
    # TODO clean up logic, account for US amazon, other price locations on page
    try:
        page = requests.get(target_url, headers=HEADERS)
        soup = BeautifulSoup(page.content, "lxml")
        title = soup.find(id="productTitle").text
        price = soup.find(class_="a-offscreen").text
        time.sleep(3)
        if title is None or price is None:
            return None
        return [float(re.sub("[^0-9.]|\.(?=.*\.)", "", price)), title.strip()]
    except Exception as error:
        print("Scrape Site function error", error)


try:
    with psycopg2.connect(my_db) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Scrapes WHERE active_search = true")
            records = cur.fetchall()
            for record in records:
                newPrice = scrape_site(record[11])
                if newPrice is None:  # if any error
                    send_mail_problem(record[2], record[11], record[3])
                    cur.execute(
                        sql.SQL(
                            "UPDATE Scrapes SET active_search = %s WHERE id=%s"
                        ).format(sql.Identifier("Scrapes")),
                        [
                            False,
                            record[0],
                        ],
                    )
                elif newPrice is not None:
                    if record[4] is None:
                        cur.execute(
                            sql.SQL(
                                "UPDATE Scrapes SET initial_price = %s, lowest_price = %s, product_name = %s, lowest_date = %s WHERE id=%s"
                            ).format(sql.Identifier("Scrapes")),
                            [
                                newPrice[0],
                                newPrice[0],
                                newPrice[1],
                                datetime.utcnow(),
                                record[0],
                            ],
                        )
                    if record[4] is None or newPrice[0] < record[5]:
                        cur.execute(
                            sql.SQL(
                                "UPDATE Scrapes SET lowest_price = %s, lowest_date = %s WHERE id=%s"
                            ).format(sql.Identifier("Scrapes")),
                            [
                                newPrice[0],
                                datetime.utcnow(),
                                record[0],
                            ],
                        )
                    if newPrice[0] < record[3]:
                        cur.execute(
                            sql.SQL(
                                "UPDATE Scrapes SET active_search = %s WHERE id=%s"
                            ).format(sql.Identifier("Scrapes")),
                            [
                                False,
                                record[0],
                            ],
                        )
                        send_mail_found(
                            record[11],
                            record[3],
                            record[2],
                            newPrice[1],
                            record[4],
                            newPrice[0],
                            record[6],
                            record[7],
                        )

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
