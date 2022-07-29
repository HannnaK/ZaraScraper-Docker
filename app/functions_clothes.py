import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from openpyxl import Workbook


def find_index(tag, class_, clothesBS):
    index_text = clothesBS.find(tag, class_).text
    index_text_list = index_text.split(" ")
    index = index_text_list[-1]
    return index


def find_old_price(clothesBS, is_on_sale):
    div = clothesBS.find("div", "product-detail-info__price-amount price")
    if is_on_sale == 1:
        old_price_span = div.find(
            "span", "price-old__amount price__amount price__amount-old"
        )
        old_price_with_currency = old_price_span.text
        old_price_text = old_price_with_currency.split(" ")[0]
        old_price = float(old_price_text.replace(",", "."))
        return old_price
    else:
        return None


def find_price(clothesBS):
    div = clothesBS.find("div", "product-detail-info__price-amount price")
    price_with_currency = div.find("span", "price-current__amount").text
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
            "div", "product-detail-color-selector product-detail-info__color-selector"
        )
        color_span = color_div.find_all("span", "screen-reader-text")
        color_list = []
        for span in color_span:
            color = span.text
            color_list.append(color)
        return sorted(color_list)
    else:
        color_text = clothesBS.find(
            "p", "product-detail-selected-color product-detail-info__color"
        ).text

        color_list = color_text.split(" ")
        if len(color_list) > 3:
            color = [color_list[0] + " " + color_list[1]]
        else:
            color = color_list[0]
            try:
                color_int = int(color[0])
                color = []
            except ValueError:
                color = [color]
        return color


def list_of_clothes(clothes_dict, list_with_all_data):
    clothes_list = []
    for key, value in clothes_dict.items():

        for clothes in list_with_all_data:
            if clothes.category == key:
                if len(clothes.colors) == 0:
                    if len(clothes.sizes) == 0:
                        clothes_list.append(
                            [
                                clothes.category,
                                clothes.index,
                                clothes.link,
                                clothes.is_on_sale,
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
                            clothes_list.append(
                                [
                                    clothes.category,
                                    clothes.index,
                                    clothes.link,
                                    clothes.is_on_sale,
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
                            clothes_list.append(
                                [
                                    clothes.category,
                                    clothes.index,
                                    clothes.link,
                                    clothes.is_on_sale,
                                    clothes.name,
                                    clothes.price,
                                    clothes.old_price,
                                    clothes.description,
                                    color,
                                    None,
                                ]
                            )
                        for size in clothes.sizes:
                            clothes_list.append(
                                [
                                    clothes.category,
                                    clothes.index,
                                    clothes.link,
                                    clothes.is_on_sale,
                                    clothes.name,
                                    clothes.price,
                                    clothes.old_price,
                                    clothes.description,
                                    color,
                                    size,
                                ]
                            )

    return clothes_list


def list_of_all_data(clothes_dict, Clothes):
    list_with_all_data = []
    for category, clothes_list in clothes_dict.items():
        for path in clothes_list:
            try:
                ua = UserAgent()
                headers = {"User-Agent": str(ua.chrome)}
                clothes_requests = requests.get(path[0], headers=headers)

                clothesBS = BeautifulSoup(clothes_requests.content, features="lxml")

                list_with_all_data.append(
                    Clothes(path[0], path[1], category, clothesBS)
                )

            except (AttributeError, TypeError):
                print("this link no longer exists or it is an ad: ", path[0])

    return list_with_all_data


def save_clothes_dict_to_exel(data, clothes_dict, data_to_exel):
    file_name = "men" + data + ".xlsx"
    wb = Workbook()
    for category, _ in clothes_dict.items():
        key = category
        wb.create_sheet(key)
        wb[key].append(
            [
                "index",
                "link",
                "wyprzedaz",
                "nazwa",
                "aktualna cena",
                "poprzednia cena",
                "opis",
                "kolor",
                "rozmiar",
            ]
        )

    for clothes_exel in data_to_exel:
        wb[clothes_exel[1]].append(
            [
                clothes_exel[2],
                clothes_exel[3],
                clothes_exel[4],
                clothes_exel[5],
                clothes_exel[6],
                clothes_exel[7],
                clothes_exel[8],
                clothes_exel[9],
                clothes_exel[10],
            ]
        )

    wb.remove(wb["Sheet"])
    wb.save(file_name)
