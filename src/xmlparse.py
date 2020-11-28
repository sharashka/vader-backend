import typing
import copy
from bs4 import BeautifulSoup, Tag


def offer_to_dict(xml_offer_tag: Tag) -> dict:
    """

    :param xml_offer_tag: An xml "offer" tag from goods export file
    :return:

    """

    children = [child for child in xml_offer_tag.children if isinstance(child, Tag)]

    params = {
        child.name: child.text
        for child in children
        if child.name not in ("store", "param")
    }

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

    params.update(freeform_params)

    result = {
        "vader_id": xml_offer_tag.attrs["id"],
        "params": params,
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
