import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from categories_man import driver


def find_index(tag, class_, clothesBS):
    index_text = clothesBS.find(tag, class_).text
    index_text_list = index_text.split(" ")
    index = index_text_list[-1]
    return index


def find_price(clothesBS):
    span = clothesBS.find("div", "product-detail-info__price-amount price")
    price_with_currency = span.find("span", "price-current__amount").text
    price_text = price_with_currency.split(" ")[0]
    num_char_price_text = 6
    if len(price_text) > num_char_price_text:
        price_text = price_text.replace("\xa0", "")
    price = float(price_text.replace(",", "."))
    return price


def find_color(clothesBS):
    if (
        clothesBS.find(
            "div", "product-detail-color-selector product-detail-info__color-selector"
        )
        != None
    ):
        color_div = clothesBS.find(
            "div",
            "product-detail-color-selector product-detail-info__color-selector",
            clothesBS,
        )
        color_span = color_div.find_all("span", "screen-reader-text")
        color_list = []
        for span in color_span:
            color = span.text
            color_list.append(color)
        return color_list
    else:
        color_text = clothesBS.find(
            "p", "product-detail-selected-color product-detail-info__color"
        ).text
        color_list = color_text.split(" ")
        color = color_list[0]
        try:
            color_int = int(color[0])
            color = []
        except ValueError:
            color = [color]
        return color


def find_prices_colors(category, clothesBS, path):
    for span in clothesBS.find_all("div", "product-detail-info__price-amount price"):
        old_price_span = span.find(
            "span", "price-old__amount price__amount price__amount-old"
        )
        if old_price_span != None:
            old_price_with_currency = old_price_span.text
            old_price_text = old_price_with_currency.split(" ")[0]
            old_price = float(old_price_text.replace(",", "."))
            price = find_price(clothesBS)
            colors = find_color(clothesBS)
            return [old_price, price, colors]

        elif old_price_span == None and category != "promocje":
            old_price = None
            colors = find_color(clothesBS)
            price = find_price(clothesBS)
            return [old_price, price, colors]
        else:
            driver.get(path)
            waiting_time = 6
            time.sleep(waiting_time)
            el = driver.find_element(
                By.XPATH,
                "//span[@class='product-detail-color-selector__color-marker']/span[@class='product-detail-color-selector__color-area']/span[@class='screen-reader-text']",
            )
            driver.execute_script("arguments[0].click();", el)
            different_colour = driver.page_source
            clothesBS_colour = BeautifulSoup(different_colour, features="lxml")

            for span in clothesBS_colour.find_all(
                "div", "product-detail-info__price-amount price"
            ):
                old_price_with_currency = span.find(
                    "span", "price-old__amount price__amount price__amount-old"
                ).text
                old_price_text = old_price_with_currency.split(" ")[0]
                old_price = float(old_price_text.replace(",", "."))
                price = find_price(clothesBS_colour)
                colors = clothesBS_colour.find(
                    "span",
                    "product-detail-color-selector__color-marker product-detail-color-selector__color-marker--is-selected",
                )
                color = [colors.find("span", "screen-reader-text").text]
                return [old_price, price, color]
