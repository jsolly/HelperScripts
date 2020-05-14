import json


def download_item_json(item):
    item_json = item.get_data()
    with open(f"{item.id}.json", "w") as outfile:
        json.dump(item_json, outfile)
