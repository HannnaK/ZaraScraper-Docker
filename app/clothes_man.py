import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime
from openpyxl import Workbook
from fake_useragent import UserAgent
from functions_man import find_index, find_old_price, find_price, find_color

conn = sqlite3.connect('database.db')
c = conn.cursor()

data_download = """
SELECT * FROM "clothes";
"""

links = c.execute(data_download)
man_clothes = links.fetchall()

only_categories = []
for category in man_clothes:
    only_categories.append(category[0])
only_categories = list(set(only_categories))

clothes_dict = {}
for category in only_categories:
    clothes_dict[category] = []

for link in man_clothes:
    clothes_dict[link[0]].append((link[1], link[2]))

data = datetime.now().strftime("%Y-%m-%d")
print(datetime.now())


class Clothes:
    def __init__(self, path, is_on_sale, category, clothesBS):
        self.category = category
        if (
                clothesBS.find(
                    "p",
                    "product-detail-selected-color product-detail-color-selector__selected-color-name",
                )
                != None
        ):
            index = find_index(
                "p",
                "product-detail-selected-color product-detail-color-selector__selected-color-name",
                clothesBS,
            )
        else:
            index = find_index(
                "p",
                "product-detail-selected-color product-detail-info__color",
                clothesBS,
            )
        self.index = index

        self.link = path

        self.is_on_sale = "nie" if is_on_sale == 0 else "tak"

        self.name = clothesBS.find("meta", property="og:title")["content"]

        self.description = clothesBS.find("meta", property="og:description")["content"]

        self.sizes = []
        for span in clothesBS.find_all("span", "product-detail-size-info__main-label"):
            size = span.text
            self.sizes.append(size)

        self.old_price = find_old_price(clothesBS, is_on_sale)
        self.price = find_price(clothesBS)
        self.colors = find_color(clothesBS)


list_with_all_data = []
for category, clothes_list in clothes_dict.items():
    for path in clothes_list:
        try:
            ua = UserAgent()
            headers = {'User-Agent': str(ua.chrome)}
            clothes_requests = requests.get(path[0], headers=headers)

            clothesBS = BeautifulSoup(clothes_requests.content, features="lxml")

            list_with_all_data.append(Clothes(path[0], path[1], category, clothesBS))

        except (AttributeError, TypeError):
            print('this link no longer exists or it is an ad: ', path[0])

print('ilość linków:', len(list_with_all_data))

file_name = 'men' + data + '.xlsx'
wb = Workbook()

for key, value in clothes_dict.items():
    wb.create_sheet(key)
    wb[key].append(
        ['index', 'link', 'wyprzedaz', 'nazwa', 'aktualna cena', 'poprzednia cena', 'opis', 'kolor', 'rozmiar'])
    for clothes in list_with_all_data:
        if clothes.category == key:
            if len(clothes.colors) == 0:
                if len(clothes.sizes) == 0:
                    wb[key].append([clothes.index, clothes.link, clothes.is_on_sale, clothes.name, clothes.price,
                                    clothes.old_price,
                                    clothes.description, None, None])
                else:
                    for size in clothes.sizes:
                        wb[key].append([clothes.index, clothes.link, clothes.is_on_sale, clothes.name, clothes.price,
                                        clothes.old_price,
                                        clothes.description, None, size])
            else:
                for color in clothes.colors:
                    if len(clothes.sizes) == 0:
                        wb[key].append([clothes.index, clothes.link, clothes.is_on_sale, clothes.name, clothes.price,
                                        clothes.old_price,
                                        clothes.description, color, None])
                    for size in clothes.sizes:
                        wb[key].append([clothes.index, clothes.link, clothes.is_on_sale, clothes.name, clothes.price,
                                        clothes.old_price,
                                        clothes.description, color, size])

wb.remove(wb['Sheet'])
wb.save(file_name)
print(datetime.now())
