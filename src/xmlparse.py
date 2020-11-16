import typing
import copy
from bs4 import BeautifulSoup, Tag


def offer_to_dict(xml_offer_tag: Tag) -> dict:
    """

    :param xml_offer_tag: An xml "offer" tag from goods export file
    :return:

    """

    children = [child for child in xml_offer_tag.children if isinstance(child, Tag)]

    top_level_params = {
        child.name: child.text
        for child in children
        if child.name not in ("store", "param")
    }

    top_level_params["vader_id"] = xml_offer_tag.attrs["id"]

    freeform_params = {
        child.attrs["name"]: child.text
        for child in xml_offer_tag
        if isinstance(child, Tag) and child.name == "param"
    }

    stores = {
        child.attrs["id"]: {"value": child.text, "store_name": child.attrs["name"]}
        for child in xml_offer_tag.children
        if child.name == "store"
    }

    result = {
        "top_level": top_level_params,
        "freeform": freeform_params,
        "stores": stores,
    }

    return result


def reform_store_dicts(_offer_dict: dict) -> typing.Tuple[dict, dict]:
    offer_dict = copy.deepcopy(_offer_dict)

    stores = offer_dict.pop("stores")

    offer_dict["inventory"] = {
        store_id: offer_store_info["value"]
        for store_id, offer_store_info in stores.items()
    }

    store_names = {
        store_id: offer_store_info["store_name"]
        for store_id, offer_store_info in stores.items()
    }

    return offer_dict, store_names


def parse_xml_string(xml_string: str) -> dict:
    parsed_xml = BeautifulSoup(xml_string, "lxml-xml")
    offers = parsed_xml.find_all("offer")

    _offer_dicts = [offer_to_dict(tag) for tag in offers]

    offers_dicts = []

    stores = {}

    for _offer_dict in _offer_dicts:
        offer_dict, store_names = reform_store_dicts(_offer_dict)
        offers_dicts.append(offer_dict)
        stores.update(store_names)

    return {"offers": offers_dicts, "stores": stores}


if __name__ == "__main__":
    example = """
   <?xml version="1.0" encoding="windows-1251"?>
   <offers>
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
				<store id="О00000003" name="ВС 1 (Толбухина)">1</store>
				<store id="О00000005" name="ВС 4 (Лента)">1</store>
				<store id="О00000006" name="ВС 5 (Флагман)">1</store>
				<store id="О00000002" name="ВС 6 (ЕвроЛэнд)">1</store>
				<store id="О00000004" name="ВС 7 (М5-Молл)">1</store>
				<store id="ЦБ0000014" name="ВС 8 (Серебряный город)">1</store>
				<store id="ЦБ0000017" name="ВС 9 (Вернисаж)">1</store>
				<store id="ЦБ0000023" name="ВС 11 (Ковров-Молл)">2</store>
				<store id="О00000007" name="Распределительный центр">9</store>
			</offer>
			<offer id="Ц0000007169">
				<аrticle>5826-Л/5226-А</аrticle>
				<name>Купальник для девочек Skat</name>
				<price>999</price>
				<НоваяКоллекция>Нет</НоваяКоллекция>
				<ЛучшийВыбор>Да</ЛучшийВыбор>
				<ЛучшаяЦена>Нет</ЛучшаяЦена>
				<param name="Размеровка">38</param>
				<param name="Сезон">SS 2019</param>
				<param name="Цвет">Розовый/голубой/желтый</param>
				<store id="О00000003" name="ВС 1 (Толбухина)">1</store>
				<store id="О00000005" name="ВС 4 (Лента)">1</store>
				<store id="О00000006" name="ВС 5 (Флагман)">1</store>
				<store id="О00000002" name="ВС 6 (ЕвроЛэнд)">1</store>
				<store id="О00000004" name="ВС 7 (М5-Молл)">1</store>
				<store id="ЦБ0000014" name="ВС 8 (Серебряный город)">1</store>
				<store id="ЦБ0000017" name="ВС 9 (Вернисаж)">1</store>
				<store id="ЦБ0000023" name="ВС 11 (Ковров-Молл)">1</store>
				<store id="О00000007" name="Распределительный центр">9</store>
			</offer>
			
   </offers>
   
   
   """
    import pprint

    pprint.pprint(parse_xml_string(example))
