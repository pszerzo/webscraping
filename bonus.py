import datetime
import requests
import selectorlib


URL = "https://programmer100.pythonanywhere.com/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}


def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["home"]
    return value


def store(extracted):
    with open("data_temp.txt", "a") as file:
        file.write(extracted + "\n")


def read(extracted):
    with open("data_temp.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)

    content = read(extracted)
    if extracted not in "data_temp.txt":
        now = datetime.datetime.now()
        store(now.strftime("%y-%m-%d-%H-%M-%S") + "," + extracted)