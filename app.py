from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import *
from datetime import datetime

# from markupsafe import escape
import re
import os

load_dotenv(find_dotenv())

app = Flask(__name__)
app.debug = os.getenv("APPDEBUGSTATE")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DBURI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/")
def index():
    return render_template("/index.html")


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
        data = Scrapes(userEmail, targetPrice, productURL)
        db.session.add(data)
        db.session.commit()
        ## TODO SEND CONFIRMATION EMAIL /W CANCEL LINK, product url, target price
        # send_confirmation_mail(productURL, targetPrice, userEmail)
        return render_template("/received.html")


# @app.route("/confirm/<int:post_id>")
# def confirm(id):
#     # TODO set up confirmation page to switch active search/email confirmation on
#     # figure out routing solution
#     # TODO DB SESSION REQUEST DATA
#     # make endpoint to cancel
#     return render_template("/confirm.html")

# EXAMPLE ROUTE
#     @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return f'Post {post_id}'


# @app.route("/cancel")
# def cancel():
#     # TODO set up confirmation page to switch active search/email confirmation on
#     # figure out routing solution
#     return render_template("/cancel.html")


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
