import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ROOT_URL = os.getenv("ROOT_URL")


def send_mail_found(
    productURL,
    targetPrice,
    userEmail,
    productName,
    initialPrice,
    currentPrice,
    startDate,
    endDate,
):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        message = f"<h3>Great News! Your product is at or below your desired price!</h3><ul><li>Product URL: {productURL}</li><li>Product Name: {productName}</li><li>Starting Price: {initialPrice}</li><li>Desired Price: {targetPrice}</li><li>Current Price: {currentPrice}</li><li>Tracking Start: {startDate}</li><li>Tracking End: {endDate}</li></ul><p>We have stopped tracking this product. Please reply to this email if you have any questions, comments, or concerns.</p>"
        msg = MIMEText(message, "html")
        msg["Subject"] = "Product Tracking Success!"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = userEmail
        smtp.sendmail(EMAIL_ADDRESS, userEmail, msg.as_string())


def send_mail_problem(userEmail, productURL, targetPrice):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        message = f"<h3>Sorry, there was an error tracking your product</h3><ul><li>Product URL: {productURL}</li><li>Desired Price: {targetPrice}</li></ul><p>We have stopped tracking this product. Please reply to this email if you have any questions, comments, or concerns.</p>"
        msg = MIMEText(message, "html")
        msg["Subject"] = "Product Tracking Error"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = userEmail
        smtp.sendmail(EMAIL_ADDRESS, userEmail, msg.as_string())


# TODO clean up email formatting
def send_mail_confirm(productURL, targetPrice, userEmail, uUserID):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        message = f"""
            <h2>Want us to let you know when this product is at your desired price?</h2>
            <ul>
                <li>Product URL: {productURL}</li>
                <li>Desired Price: {targetPrice}</li>
            </ul>
            <p>Simply click the link below and we'll check the price daily. Once it is at or below your desired price, we'll send you another email.</p>
            <h3> <a href="{ROOT_URL}confirm/{uUserID}">Click here to confirm</a></h3>
            <p>If at any time you want to stop tracking this product click the link below.</p>
            <h3> <a href="{ROOT_URL}cancel/{uUserID}">Click here to cancel</a></h3>
            """
        msg = MIMEText(message, "html")
        msg["Subject"] = "Product Tracking Confirmation Required"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = userEmail
        smtp.sendmail(EMAIL_ADDRESS, userEmail, msg.as_string())
