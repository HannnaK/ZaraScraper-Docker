import sqlite3

conn = sqlite3.connect("database.db")


def database_connection(query, parameters):
    c = conn.cursor()
    result = c.execute(query, parameters)
    return result


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
        return color_list
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
