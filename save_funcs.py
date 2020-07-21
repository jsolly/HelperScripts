import json


def download_item_json(item, save_location=None):
    item_json = item.get_data()
    save_location = (
        f"{item.id}.json" if not save_location else f"{save_location}{item.id}.json"
    )

    with open(save_location, "w") as outfile:
        json.dump(item_json, outfile)
