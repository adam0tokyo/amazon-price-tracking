import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


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


# TODO send_mail_confirm
