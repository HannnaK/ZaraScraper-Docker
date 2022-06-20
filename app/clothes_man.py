import requests
from bs4 import BeautifulSoup
from datetime import datetime
from openpyxl import Workbook
from fake_useragent import UserAgent
from categories_man import categories_dict
from functions_man import find_index, find_prices_colors

data = datetime.now().strftime("%Y-%m-%d")
print(datetime.now())


class Clothes:
    def __init__(self, path, category, clothesBS):
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

        self.name = clothesBS.find("meta", property="og:title")["content"]

        self.description = clothesBS.find("meta", property="og:description")["content"]

        self.sizes = []
        for span in clothesBS.find_all("span", "product-detail-size-info__main-label"):
            size = span.text
            self.sizes.append(size)

        prices_colors = find_prices_colors(category, clothesBS, path)

        self.old_price = prices_colors[0]
        self.price = prices_colors[1]
        self.colors = prices_colors[2]


list_with_all_data = []
for category, clothes_list in categories_dict.items():

    for path in clothes_list:
        try:
            ua = UserAgent()
            headers = {"User-Agent": str(ua.chrome)}
            clothes_requests = requests.get(path, headers=headers)

            clothesBS = BeautifulSoup(clothes_requests.content, features="lxml")

            list_with_all_data.append(Clothes(path, category, clothesBS))

        except (AttributeError, TypeError):
            print("link does not exist or is an ad: ", path)

print("quantity of links:", len(list_with_all_data))

file_name = "men" + data + ".xlsx"
wb = Workbook()

for key, value in categories_dict.items():
    wb.create_sheet(key)
    wb[key].append(
        [
            "index",
            "link",
            "nazwa",
            "aktualna cena",
            "poprzednia cena",
            "opis",
            "kolor",
            "rozmiar",
        ]
    )
    for clothes in list_with_all_data:
        if clothes.category == key:
            if len(clothes.colors) == 0:
                if len(clothes.sizes) == 0:
                    wb[key].append(
                        [
                            clothes.index,
                            clothes.link,
                            clothes.name,
                            clothes.price,
                            clothes.old_price,
                            clothes.description,
                            None,
                            None,
                        ]
                    )
                else:
                    for size in clothes.sizes:
                        wb[key].append(
                            [
                                clothes.index,
                                clothes.link,
                                clothes.name,
                                clothes.price,
                                clothes.old_price,
                                clothes.description,
                                None,
                                size,
                            ]
                        )
            else:
                for color in clothes.colors:
                    if len(clothes.sizes) == 0:
                        wb[key].append(
                            [
                                clothes.index,
                                clothes.link,
                                clothes.name,
                                clothes.price,
                                clothes.old_price,
                                clothes.description,
                                color,
                                None,
                            ]
                        )
                    for size in clothes.sizes:
                        wb[key].append(
                            [
                                clothes.index,
                                clothes.link,
                                clothes.name,
                                clothes.price,
                                clothes.old_price,
                                clothes.description,
                                color,
                                size,
                            ]
                        )

wb.remove(wb["Sheet"])
wb.save(file_name)
print(datetime.now())
