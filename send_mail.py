import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


# def send_mail_old(productURL, targetPrice, userEmail, currentPrice):
#     port = os.getenv("MALPORT")
#     smtp_server = os.getenv("SMTPSERVER")
#     login = os.getenv("MAILUSERNAME")
#     password = os.getenv("MAILPASSWORD")
#     message = f"<h3>Test EMAIL</h3><ul><li>Product URL: {productURL}</li><li>Desired Price: {targetPrice}</li><li>user Email: {userEmail}</li><li>Current Price: {currentPrice}</li></ul>"

#     sender_email = "simplepricetracking@gmail.com"
#     receiver_email = "{userEmail}"
#     msg = MIMEText(message, "html")
#     msg["Subject"] = "Confrim Test"
#     msg["From"] = "simplepricetracking@gmail.com"
#     msg["To"] = userEmail

#     # Send email
#     with smtplib.SMTP(smtp_server, port) as server:
#         server.login(login, password)
#         server.sendmail(sender_email, receiver_email, msg.as_string())


##ALTERNATE USING GOOGLE
# SSL??  https://www.youtube.com/watch?v=g_j6ILT-X0k NO, USE TLS

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_mail(productURL, targetPrice, userEmail, currentPrice):
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject = "Testing 4..5..6.."
        body = f"<h3>Test EMAIL</h3><ul><li>Product URL: {productURL}</li><li>Desired Price: {targetPrice}</li><li>user Email: {userEmail}</li><li>Current Price: {currentPrice}</li></ul>"

        msg = f"Subject: {subject}\n\n{body}"

        smtp.sendmail(EMAIL_ADDRESS, userEmail, msg)


# send_mail()
# send_mail("FAKEURL", "TARGET PRICE 5", "test@MAIL.com", "currentPrice 500")
