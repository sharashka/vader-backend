import unittest
from src import __version__
import src.xmlparse as xmlparse
from bs4 import BeautifulSoup, Tag


def to_bs_tag(tag_name: str, xml_string: str) -> Tag:
    parsed_xml = BeautifulSoup(xml_string, "lxml-xml")
    offer = parsed_xml.find(tag_name)
    return offer


class TestHelpers(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_version(self):
        assert __version__ == "0.1.0"

    def test_offer_to_dict(self):
        self.assertEqual(
            xmlparse.offer_to_dict(
                to_bs_tag(
                    "offer",
                    """
                    <offer id="Ц0000007168">
                    <аrticle>5826-Л/5226-А</аrticle>
                    <name>Купальник для девочек Skat</name>
                    <price>999</price>
                    <НоваяКоллекция>Нет</НоваяКоллекция>
                    <ЛучшийВыбор>Да</ЛучшийВыбор>
                    <ЛучшаяЦена>Нет</ЛучшаяЦена>
                    <param name="Размеровка">36</param>
                    <param name="Сезон">SS 2019</param>
                    <param name="Цвет">Розовый/голубой/желтый</param>
                    <store id="О00000002" name="ВС 6 (ЕвроЛэнд)">1</store>
                    <store id="ЦБ0000014" name="ВС 8 (Серебряный город)">1</store>
                    </offer>
                """,
                )
            ),
            {
                "params": {
                    "name": "Купальник для девочек Skat",
                    "price": "999",
                    "ЛучшаяЦена": "Нет",
                    "ЛучшийВыбор": "Да",
                    "НоваяКоллекция": "Нет",
                    "Размеровка": "36",
                    "Сезон": "SS 2019",
                    "Цвет": "Розовый/голубой/желтый",
                    "аrticle": "5826-Л/5226-А",
                },
                "stores": {
                    "О00000002": {"store_name": "ВС 6 (ЕвроЛэнд)", "value": "1"},
                    "ЦБ0000014": {
                        "store_name": "ВС 8 (Серебряный город)",
                        "value": "1",
                    },
                },
                "vader_id": "Ц0000007168",
            },
        )

    def test_reform_store_dicts(self):
        self.assertEqual(
            xmlparse.reform_store_dicts(
                {
                    "params": {
                        "name": "Купальник для девочек Skat",
                        "аrticle": "5826-Л/5226-А",
                    },
                    "stores": {
                        "О00000002": {"store_name": "ВС 6 (ЕвроЛэнд)", "value": "1"},
                        "ЦБ0000014": {
                            "store_name": "ВС 8 (Серебряный город)",
                            "value": "1",
                        },
                    },
                    "vader_id": "Ц0000007168",
                }
            ),
            (
                {
                    "inventory": {
                        "О00000002": "1",
                        "ЦБ0000014": "1",
                    },
                    "params": {
                        "name": "Купальник для девочек Skat",
                        "аrticle": "5826-Л/5226-А",
                    },
                    "vader_id": "Ц0000007168",
                },
                {
                    "О00000002": "ВС 6 (ЕвроЛэнд)",
                    "ЦБ0000014": "ВС 8 (Серебряный город)",
                },
            ),
        )

    def test_parse_xml_string(self):
        self.assertEqual(
            xmlparse.parse_xml_string(xmlparse.example),
            {
                "offers": [
                    {
                        "inventory": {
                            "О00000002": "1",
                            "О00000003": "1",
                            "О00000004": "1",
                            "О00000005": "1",
                            "О00000006": "1",
                            "О00000007": "9",
                            "ЦБ0000014": "1",
                            "ЦБ0000017": "1",
                            "ЦБ0000023": "2",
                        },
                        "params": {
                            "name": "Купальник для девочек Skat",
                            "price": "999",
                            "ЛучшаяЦена": "Нет",
                            "ЛучшийВыбор": "Да",
                            "НоваяКоллекция": "Нет",
                            "Размеровка": "36",
                            "Сезон": "SS 2019",
                            "Цвет": "Розовый/голубой/желтый",
                            "аrticle": "5826-Л/5226-А",
                        },
                        "vader_id": "Ц0000007168",
                    },
                    {
                        "inventory": {
                            "О00000002": "1",
                            "О00000003": "1",
                            "О00000004": "1",
                            "О00000005": "1",
                            "О00000006": "1",
                            "О00000007": "9",
                            "ЦБ0000014": "1",
                            "ЦБ0000017": "1",
                            "ЦБ0000023": "1",
                        },
                        "params": {
                            "name": "Купальник для девочек Skat",
                            "price": "999",
                            "ЛучшаяЦена": "Нет",
                            "ЛучшийВыбор": "Да",
                            "НоваяКоллекция": "Нет",
                            "Размеровка": "38",
                            "Сезон": "SS 2019",
                            "Цвет": "Розовый/голубой/желтый",
                            "аrticle": "5826-Л/5226-А",
                        },
                        "vader_id": "Ц0000007169",
                    },
                ],
                "stores": {
                    "О00000002": "ВС 6 (ЕвроЛэнд)",
                    "О00000003": "ВС 1 (Толбухина)",
                    "О00000004": "ВС 7 (М5-Молл)",
                    "О00000005": "ВС 4 (Лента)",
                    "О00000006": "ВС 5 (Флагман)",
                    "О00000007": "Распределительный центр",
                    "ЦБ0000014": "ВС 8 (Серебряный город)",
                    "ЦБ0000017": "ВС 9 (Вернисаж)",
                    "ЦБ0000023": "ВС 11 (Ковров-Молл)",
                },
            },
        )
