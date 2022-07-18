from base_init import run_script_sql
from categories_man import categories_man_fun
from clothes_man import clothes_man_fun


if __name__ == "__main__":
    run_script_sql(
        [
            "migrations/categories.sql",
            "migrations/clothes.sql",
            "migrations/clothes_details.sql",
        ]
    )
    categories_man_fun()
    clothes_man_fun()
