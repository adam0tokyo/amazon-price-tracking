from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from send_mail import send_mail_confirm
from datetime import datetime
import uuid
import re
import os


load_dotenv(find_dotenv())

app = Flask(__name__)
app.debug = os.getenv("APPDEBUGSTATE")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DBURI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Scrapes(db.Model):
    __tablename__ = "scrapes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    user_email = db.Column(db.String(1000), nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    initial_price = db.Column(db.Float)
    lowest_price = db.Column(db.Float)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    lowest_date = db.Column(db.DateTime, default=datetime.utcnow)
    email_confirmed = db.Column(db.Boolean, default=False)
    active_search = db.Column(db.Boolean, default=False)
    product_name = db.Column(db.String(1000))
    product_url = db.Column(db.String(5000), nullable=False)

    def __init__(self, userEmail, targetPrice, productURL, uUserID):
        self.user_email = userEmail
        self.target_price = float(targetPrice)
        self.product_url = productURL
        self.user_id = uUserID


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
        uUserID = uuid.uuid4()
        if (
            ("amazon.co.jp" not in productURL)
            and ("amazon.jp" not in productURL)
            # ("amazon.com" not in productURL)
        ):
            return render_template(
                "index.html",
                message="Sorry, currently we only support amazon.co.jp",
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
        data = Scrapes(userEmail, targetPrice, productURL, uUserID)
        db.session.add(data)
        db.session.commit()
        send_mail_confirm(productURL, targetPrice, userEmail, uUserID)
        return render_template("/received.html")


@app.route("/confirm/<target_user>")
def confirm(target_user):
    print("test", uuid.uuid4())
    record = Scrapes.query.filter_by(user_id=target_user).first_or_404()
    record.email_confirmed = True
    record.active_search = True
    db.session.commit()
    return render_template("/confirm.html")


@app.route("/cancel/<target_user>")
def cancel(target_user):
    record = Scrapes.query.filter_by(user_id=target_user).first_or_404()
    record.active_search = False
    db.session.commit()
    print(app)
    return render_template("/cancel.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
