import time
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup


def all_hrefs(column_number, clothing, path):
    all_href = []
    for column in column_number:
        all_li_column = clothing.find_all("li", column)
        for li in all_li_column:
            data_productid = li["data-productid"]
            li_a = li.find("a")
            href = li_a.get("href")
            whole_href = href + "?v1=" + data_productid + "&v2=" + path[-7:]
            all_href.append(whole_href)
    return all_href


driver = webdriver.Remote(
    command_executor=os.environ["PATH_DRIVER"],
    desired_capabilities=DesiredCapabilities.CHROME,
)


def create_categories_dict(man_categories, categories_dict):
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
    driver.close()
    return categories_dict
