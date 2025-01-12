import requests
import selectorlib
import smtplib
import ssl
import os
import time
import sqlite3


URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

connection = sqlite3.connect("data.db")


def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, name = row
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()

def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, name = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                   (band, city, name))
    rows = cursor.fetchall()
    print(rows)
    return rows


def send_email(message, receiver="peterszerzo@gmail.com", username="peterszerzo@gmail.com"):
    mycontext = ssl.create_default_context()
    host = "smtp.gmail.com"
    port = 465
    pw = os.getenv("PASSWORD")
    mycontext = ssl.create_default_context()

    with smtplib.SMTP_SSL(host=host, port=port, context=mycontext) as server:
        server.login(username, pw)
        server.sendmail(username, receiver, message)


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message="new event")
        time.sleep(2)