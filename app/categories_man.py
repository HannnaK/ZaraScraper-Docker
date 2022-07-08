import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from datetime import datetime
from functions_man import all_hrefs

print(datetime.now())


def categories_man_fun():
    driver = webdriver.Remote(
        "http://selenium:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME
    )

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    data_download = """
    SELECT * FROM "categories";
    """
    links = c.execute(data_download)
    man_categories = links.fetchall()

    only_categories = []
    for category in man_categories:
        only_categories.append(category[0])
    only_categories = list(set(only_categories))

    categories_dict = {}
    for category in only_categories:
        categories_dict[category] = []

    for category in man_categories:
        path = category[1]
        is_on_sale = category[2]
        print(category[0], category[2])
        driver.get(path)

        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        zara = driver.page_source

        clothing = BeautifulSoup(zara, features="lxml")

        if is_on_sale == 1:
            column_number = [
                "product-grid-product _product product-grid-product--ZOOM1-columns product-grid-product--0th-column",
                "product-grid-product _product product-grid-product--ZOOM1-columns product-grid-product--1th-column",
                "product-grid-product _product product-grid-product--ZOOM1-columns product-grid-product--2th-column",
                "product-grid-product _product product-grid-product--ZOOM1-columns product-grid-product--3th-column",
            ]
            hrefs = all_hrefs(column_number, clothing, path)

            for href in hrefs:
                categories_dict[category[0]].append((href, is_on_sale))
        else:
            links = clothing.find_all(
                "a", class_="product-link product-grid-product__link link"
            )
            hrefs = []
            for link in links:
                href = link.get("href")
                hrefs.append(href)
            hrefs = list(set(hrefs))
            for href in hrefs:
                categories_dict[category[0]].append((href, is_on_sale))

    for key, value in categories_dict.items():
        category = key
        for cl in value:
            clothes = cl[0]
            is_on_sale = cl[1]
            add_data = 'INSERT INTO "clothes" ("category", "clothes", "is_on_sale") VALUES (?, ?, ?)'
            parameters = (category, clothes, is_on_sale)
            c.execute(add_data, parameters)

    conn.commit()
