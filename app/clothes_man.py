from datetime import datetime

from functions_man import (
    database_connection,
    conn,
)
from functions_clothes import (
    find_index,
    find_old_price,
    find_price,
    find_color,
    list_of_clothes,
    list_of_all_data,
    save_clothes_dict_to_exel,
)


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
        for div in clothesBS.find_all("div", {"aria-label": "Wybierz rozmiar"}):
            for span in div.find_all("span", "product-detail-size-info__main-label"):
                size = span.text
                self.sizes.append(size)

        self.old_price = find_old_price(clothesBS, is_on_sale)
        self.price = find_price(clothesBS)
        self.colors = find_color(clothesBS)


def clothes_man_fun():

    data_download = """
       SELECT * FROM "clothes";
       """

    links = database_connection(data_download, ())
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

    list_with_all_data = list_of_all_data(clothes_dict, Clothes)

    print("ilość linków:", len(list_with_all_data))

    clothes_list = list_of_clothes(clothes_dict, list_with_all_data)

    for cloth in clothes_list:
        add_data = 'INSERT INTO "clothes_details" ("id", "category", "index", "link", "is_on_sale", "name", "price", "old_price", "description", "colors", "sizes") VALUES (Null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        parameters = (
            cloth[0],
            cloth[1],
            cloth[2],
            cloth[3],
            cloth[4],
            cloth[5],
            cloth[6],
            cloth[7],
            cloth[8],
            cloth[9],
        )
        database_connection(add_data, parameters)

    conn.commit()

    delete_duplicates = """
           DELETE FROM clothes_details
           WHERE rowid not in (SELECT  min(rowid) FROM clothes_details GROUP BY "category", "index", "colors", "sizes")
       """
    database_connection(delete_duplicates, ())

    without_duplicates = """
               SELECT * FROM "clothes_details";
               """

    exel_data = database_connection(without_duplicates, ())
    data_to_exel = exel_data.fetchall()

    conn.close()

    save_clothes_dict_to_exel(data, clothes_dict, data_to_exel)

    print(datetime.now())
