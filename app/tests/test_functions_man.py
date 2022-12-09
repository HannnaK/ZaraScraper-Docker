import unittest
from bs4 import BeautifulSoup
from app.variable import web_html
from app.functions_clothes import find_index, find_old_price, find_price, find_color


class TestClothes(unittest.TestCase):
    bs = None

    @classmethod
    def setUpClass(cls):
        TestClothes.bs = BeautifulSoup(web_html, features="lxml")

    def test_find_index(self):
        self.assertEqual(
            find_index(
                "p",
                "product-detail-selected-color product-detail-color-selector__selected-color-name",
                TestClothes.bs,
            ),
            "0775/411",
        )

    def test_find_old_price_is_on_sale(self):
        self.assertEqual(find_old_price(TestClothes.bs, 1), 99.90)

    def test_find_price(self):
        self.assertEqual(find_price(TestClothes.bs), 49.90)

    def test_find_color(self):
        self.assertEqual(find_color(TestClothes.bs), ["Czarny", "Zieleń butelkowa"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
