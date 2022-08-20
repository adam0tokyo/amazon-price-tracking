# from email import message
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import re
import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

app = Flask(__name__)
app.debug = os.getenv("APPDEBUGSTATE")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DBURI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/")
def index():
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
        return render_template("received.html")


db = SQLAlchemy(app)


class Scrapes(db.Model):
    __tablename__ = "scrapes"
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(1000), nullable=False)
    target_price = db.Column(db.Numeric(scale=2), nullable=False)
    product_url = db.Column(db.String(5000), nullable=False)
    initial_price = db.Column(db.Numeric(scale=2))
    lowest_price = db.Column(db.Numeric(scale=2))
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    lowest_date = db.Column(db.DateTime, default=datetime.utcnow)
    email_confirmed = db.Column(db.Boolean, default=False)
    active_search = db.Column(db.Boolean, default=False)

    def __init__(self, userEmail, targetPrice, productURL):
        self.user_email = userEmail
        self.target_price = float(targetPrice)
        self.product_url = productURL


if __name__ == "__main__":
    app.debug = True
    app.run()
