from datetime import datetime
from functions_man import database_connection, conn
from functions_categories import create_categories_dict

print(datetime.now())


def categories_man_fun():
    data_download = """
    SELECT * FROM "categories";
    """
    links = database_connection(data_download, ())

    man_categories = links.fetchall()

    only_categories = []
    for category in man_categories:
        only_categories.append(category[0])
    only_categories = list(set(only_categories))

    categories_dict = {}
    for category in only_categories:
        categories_dict[category] = []

    categories_dict = create_categories_dict(man_categories, categories_dict)

    for key, value in categories_dict.items():
        category = key
        for cl in value:
            clothes = cl[0]
            is_on_sale = cl[1]
            add_data = 'INSERT INTO "clothes" ("category", "clothes", "is_on_sale") VALUES (?, ?, ?)'
            parameters = (category, clothes, is_on_sale)
            database_connection(add_data, parameters)

    conn.commit()
