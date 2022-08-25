# from email import message
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import re
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from send_mail import send_mail

# import random

# from sqlalchemy import select
# from sqlalchemy.orm import Session

# session = Session(engine, future=True)


#  FFFFFFF
load_dotenv(find_dotenv())

app = Flask(__name__)
app.debug = os.getenv("APPDEBUGSTATE")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DBURI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/")
def index():
    # all_scrapes = db.Query.all()
    # print("TESTER", all_scrapes)

    # session.query(Scrapes)
    # for scrape in Scrapes:
    # print(scrape.user_email)
    # all_scrapes = Scrapes.query.all()
    # filtered_scrapes = Scrapes.query.filter_by(id="3").first()
    # # for item in filtered_scrapes:
    # #     print(item)
    # # print(all_scrapes, filtered_scrapes.id, filtered_scrapes.user_email)
    # for scrape in all_scrapes:
    #     print(scrape.id, scrape.user_email)
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        productURL = request.form["product-url"]
        stageTargetPrice = request.form["target-price"]
        targetPrice = re.sub("[^0-9.]|\.(?=.*\.)", "", stageTargetPrice)
        userEmail = request.form["user-email"]
        if (
            ("amazon.com" not in productURL)
            and ("amazon.co.jp" not in productURL)
            and ("amazon.jp" not in productURL)
        ):
            return render_template(
                "index.html",
                message="Sorry, currently we only support amazon.com & amazon.co.jp",
                prevProductURL=productURL,
                prevTargetPrice=stageTargetPrice,
                prevUserEmail=userEmail,
            )
        if (targetPrice == "") or (float(targetPrice) <= 0):
            return render_template(
                "index.html",
                message="Please input a valid desired price for this product.",
                prevProductURL=productURL,
                prevTargetPrice=stageTargetPrice,
                prevUserEmail=userEmail,
            )
        print(productURL, targetPrice, userEmail)
        # TODO add filter conditional for same email/prodcut/tPrice ?
        data = Scrapes(userEmail, targetPrice, productURL)
        db.session.add(data)
        db.session.commit()
        # send_mail(productURL, targetPrice, userEmail)
        return render_template("/received.html")


# @app.route("/track")
# def track():
#     all_scrapes = db.session.query.all()
#     print(all_scrapes)
# return render_template("index.html")
# @app.route("/track")
# def show_all():
#     return render_template("show_all.html", list=Scrapes.query.all())


db = SQLAlchemy(app)


class Scrapes(db.Model):
    __tablename__ = "scrapes"
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(1000), nullable=False)
    target_price = db.Column(db.Numeric(scale=2), nullable=False)
    initial_price = db.Column(db.Numeric(scale=2))
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    lowest_price = db.Column(db.Numeric(scale=2))
    lowest_date = db.Column(db.DateTime, default=datetime.utcnow)
    email_confirmed = db.Column(db.Boolean, default=False)
    active_search = db.Column(db.Boolean, default=True)
    product_name = db.Column(db.String(1000))
    product_url = db.Column(db.String(5000), nullable=False)

    def __init__(self, userEmail, targetPrice, productURL):
        self.user_email = userEmail
        self.target_price = float(targetPrice)
        self.product_url = productURL


if __name__ == "__main__":
    app.debug = True
    app.run()
