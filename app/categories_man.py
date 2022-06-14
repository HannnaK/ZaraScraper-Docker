import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from zara_main import man_categories

driver = webdriver.Remote(
    "http://selenium:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME
)

categories_dict = {}
for category in man_categories:
    path = category[1]
    print(category[0])
    driver.get(path)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(15)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    zara = driver.page_source
    clothing = BeautifulSoup(zara, features="lxml")
    links = clothing.find_all(
        "a", class_="product-link product-grid-product__link link"
    )
    links_href = []
    for link in links:
        href = link.get("href")
        links_href.append(href)
    links_href = set(links_href)
    links_href = list(links_href)
    categories_dict[category[0]] = links_href
