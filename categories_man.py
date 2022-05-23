import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
from zara import man_categories

s = Service('C://Users/kotek/Desktop/chromedriver.exe')
driver = webdriver.Chrome(service=s)

categories_dict = {}
for category in man_categories:
    path = category[1]
    print(category[0])
    driver.get(path)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    zara = driver.page_source
    clothing = BeautifulSoup(zara, features="lxml")
    links = clothing.find_all('a', class_="product-link product-grid-product__link link")
    links_href = []
    for link in links:
        href = link.get('href')
        links_href.append(href)
    links_href = set(links_href)
    links_href = list(links_href)
    categories_dict[category[0]] = links_href

driver.close()

conn = sqlite3.connect('database.db')
c = conn.cursor()

create_table = """
DROP TABLE IF EXISTS "categories";
CREATE TABLE "categories"
(
    "category" TEXT    NOT NULL,
    "clothes" TEXT    NOT NULL
);"""
c.executescript(create_table)

for key, value in categories_dict.items():
    category = key
    for cl in value:
        clothes = cl
        add_data = 'INSERT INTO "categories" ("category", "clothes") VALUES (?, ?)'
        parameters = (category, clothes)
        c.execute(add_data, parameters)

conn.commit()

conn.close()
