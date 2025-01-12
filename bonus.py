import datetime
import time

import requests
import selectorlib
import sqlite3


URL = "https://programmer100.pythonanywhere.com/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

connection = sqlite3.connect("data_temp.db")


def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["home"]
    return value


def store(extracted):
    now = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO temperature VALUES(?,?)", (now, extracted))
    connection.commit()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        store(extracted)
        time.sleep(1)