import requests
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from datetime import datetime
from openpyxl import Workbook
from fake_useragent import UserAgent
from categories_man import driver, categories_dict

data = datetime.now().strftime("%Y-%m-%d")
print(datetime.now())


def find_index(tag, class_, clothesBS):
    index_text = clothesBS.find(tag, class_).text
    index_text_list = index_text.split(' ')
    index = index_text_list[-1]
    return index


def find_price(clothesBS):
    span = clothesBS.find("div", "product-detail-info__price-amount price")
    price_with_currency = span.find("span", "price-current__amount").text
    price_text = price_with_currency.split(' ')[0]
    if len(price_text) > 6:
        price_text = price_text.replace('\xa0', '')
    price = float(price_text.replace(',', '.'))
    return price


def find_color(clothesBS):
    if clothesBS.find("div",
                      "product-detail-color-selector product-detail-info__color-selector") != None:
        color_div = clothesBS.find("div",
                                   "product-detail-color-selector product-detail-info__color-selector", clothesBS)
        color_span = color_div.find_all("span", "screen-reader-text")
        color_list = []
        for span in color_span:
            color = span.text
            color_list.append(color)
        return color_list
    else:
        color_text = clothesBS.find("p",
                                    "product-detail-selected-color product-detail-info__color").text
        color_list = color_text.split(' ')
        color = color_list[0]
        try:
            color_int = int(color[0])
            color = []
        except ValueError:
            color = [color]
        return color


def find_prices_colors(category, clothesBS, path):
    for span in clothesBS.find_all("div", "product-detail-info__price-amount price"):
        old_price_span = span.find("span", "price-old__amount price__amount price__amount-old")
        if old_price_span != None:
            old_price_with_currency = old_price_span.text
            old_price_text = old_price_with_currency.split(' ')[0]
            old_price = float(old_price_text.replace(',', '.'))
            price = find_price(clothesBS)
            colors = find_color(clothesBS)
            return [old_price, price, colors]

        elif old_price_span == None and category != 'promocje':
            old_price = None
            colors = find_color(clothesBS)
            price = find_price(clothesBS)
            return [old_price, price, colors]
        else:
            driver.get(path)

            time.sleep(6)
            el = driver.find_element(By.XPATH,
                                     "//span[@class='product-detail-color-selector__color-marker']/span[@class='product-detail-color-selector__color-area']/span[@class='screen-reader-text']")
            driver.execute_script("arguments[0].click();", el)
            different_colour = driver.page_source
            clothesBS_colour = BeautifulSoup(different_colour, features="lxml")

            for span in clothesBS_colour.find_all("div", "product-detail-info__price-amount price"):
                old_price_with_currency = span.find("span",
                                                    "price-old__amount price__amount price__amount-old").text
                old_price_text = old_price_with_currency.split(' ')[0]
                old_price = float(old_price_text.replace(',', '.'))
                price = find_price(clothesBS_colour)
                colors = clothesBS_colour.find("span",
                                               "product-detail-color-selector__color-marker product-detail-color-selector__color-marker--is-selected")
                color = [colors.find("span", "screen-reader-text").text]
                return [old_price, price, color]


class Clothes:
    def __init__(self, path, category, clothesBS):
        self.category = category
        if clothesBS.find('p',
                          "product-detail-selected-color product-detail-color-selector__selected-color-name") != None:
            index = find_index("p",
                               "product-detail-selected-color product-detail-color-selector__selected-color-name",
                               clothesBS)
        else:
            index = find_index("p", "product-detail-selected-color product-detail-info__color", clothesBS)
        self.index = index

        self.link = path

        self.name = clothesBS.find('meta', property="og:title")['content']

        self.description = clothesBS.find('meta', property="og:description")['content']

        self.sizes = []
        for span in clothesBS.find_all("span", "product-detail-size-info__main-label"):
            size = span.text
            self.sizes.append(size)

        prices_colors = find_prices_colors(category, clothesBS, path)

        self.old_price = prices_colors[0]
        self.price = prices_colors[1]
        self.colors = prices_colors[2]

    def __repr__(self):
        return f'index {self.index}, link {self.link}, name {self.name}, price {self.price}, old_price {self.old_price}, description: {self.description}, colors {self.colors}, sizes {self.sizes}'


list_with_all_data = []
for category, clothes_list in categories_dict.items():

    for path in clothes_list:
        try:
            ua = UserAgent()
            headers = {'User-Agent': str(ua.chrome)}
            clothes_requests = requests.get(path, headers=headers)

            clothesBS = BeautifulSoup(clothes_requests.content, features="lxml")

            list_with_all_data.append(Clothes(path, category, clothesBS))

        except (AttributeError, TypeError):
            print('link does not exist or is an ad: ', path)

print('ilość linków:', len(list_with_all_data))

file_name = 'men' + data + '.xlsx'
wb = Workbook()

for key, value in categories_dict.items():
    wb.create_sheet(key)
    wb[key].append(
        ['index', 'link', 'nazwa', 'aktualna cena', 'poprzednia cena', 'opis', 'kolor', 'rozmiar'])
    for clothes in list_with_all_data:
        if clothes.category == key:
            if len(clothes.colors) == 0:
                if len(clothes.sizes) == 0:
                    wb[key].append([clothes.index, clothes.link, clothes.name, clothes.price, clothes.old_price,
                                    clothes.description, None, None])
                else:
                    for size in clothes.sizes:
                        wb[key].append([clothes.index, clothes.link, clothes.name, clothes.price, clothes.old_price,
                                        clothes.description, None, size])
            else:
                for color in clothes.colors:
                    if len(clothes.sizes) == 0:
                        wb[key].append([clothes.index, clothes.link, clothes.name, clothes.price, clothes.old_price,
                                        clothes.description, color, None])
                    for size in clothes.sizes:
                        wb[key].append([clothes.index, clothes.link, clothes.name, clothes.price, clothes.old_price,
                                        clothes.description, color, size])

wb.remove(wb['Sheet'])
wb.save(file_name)
print(datetime.now())
