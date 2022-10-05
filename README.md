# simple price tracking

A basic web app for users to check amazon.co.jp products. Users can add a product URL, desired price, and their email address. Upon email confirmation, the app will check the product price daily until it is at or below the user’s desired price. When the desired price is met, the app will send the user an email alerting about the price, along with some extra information.

# Local Deployment

- clone the repo, `pipenv install` or `pip install` in your terminal
- create a `.env` file, see below for variable names and example
- create a PostgreSQL database for the project
- enable SMTP mail and get the information for your mail server
- add variables to `.env` file
- run `python`
- in python, `from app import db` then `db.create_all()` to create the database
- `python app.py` to start the web app
- run `python price_track.py` to process the requests, or schedule it to run at an interval

## .env variables

```
APPDEBUGSTATE= //True or False, depending on local or hosted deployment
DBURI= //Postgres database URI
SMTP_SERVER= //mail server name
SMTP_PORT= //mail server port
EMAIL_ADDRESS= //mail server login
EMAIL_PASSWORD= //mail server password
ROOT_URL= //app deployment URL
```

## .env example

```
APPDEBUGSTATE=True
DBURI=postgresql://postgres:mypass@localhost/simple-price-tracking
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=email_sent_from_here@gmail.com
EMAIL_PASSWORD=abcd1234
ROOT_URL=http://127.0.0.1:5000/
```

# Features

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- psycopg2
- Beautiful Soup4
- requests
- send_mail

## Images

![index](./img/index.png)

![recieved](./img/recieved.png)

![confirmation mail](./img/confirmation_mail.png)

![confirmed](./img/confirmed.png)

![success](./img/success.png)


# Feedback

Feel free to contact me by email, `adam0tokyo` at `gmail` for any questions or comments!