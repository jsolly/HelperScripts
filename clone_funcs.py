from pathlib import Path
import json
from arcgis import mapping, features
from GitHub.HelperScripts import get_funcs
from other.my_secrets import get_regression_devext_dbqa_gis


def clone_folder(
    source_folder,
    target_folder,
    source_gis,
    target_gis,
    copy_data=True,
    search_existing_items=True,
    ignore_item_type=None,
):  # Make sure copy_data=true, folder, search_existing_items are set correctly

    items_list = source_gis.users.me.items(folder=source_folder)

    if ignore_item_type:
        for item in items_list:
            if item.type in ignore_item_type:
                items_list.remove(item)

        for item in items_list:
            target_gis.content.clone_items(
                items=[item],
                folder=target_folder,
                copy_data=copy_data,
                search_existing_items=search_existing_items,
            )


def clone_group(
    source_group,
    target_group,
    target_folder,
    source_gis,
    target_gis,
    search_existing_items=True,
):
    source_group_items = source_gis.groups.search(query=source_group)[0].content()
    target_group = target_gis.groups.search(query=target_group)[0]

    for item in source_group_items:
        target_gis.content.clone_items(
            items=[item],
            folder=target_folder,
            copy_data=True,
            search_existing_items=search_existing_items,
        )

    target_folder_items = get_funcs.get_items_from_folder(
        gis_obj=target_gis, folder=target_folder
    )

    for item in target_folder_items:
        item.share(groups=[target_group])


def weak_clone_items(items: list, target_gis, target_folder, flip_https):
    for item in items:
        if not item.url:
            return

        if flip_https:
            item_url = item.url
            item_url = item_url.replace("https", "http")
        else:
            item_url = item.url

        item_properties = {"type": item.type, "title": item.title, "url": item_url}

        target_gis.content.add(
            item_properties=item_properties, data=item_url, folder=target_folder
        )


def clone_folders(source_gis, target_gis):
    source_folders = source_gis.users.me.folders
    for folder in source_folders:
        target_gis.users.me.create_folder(folder=folder)
        clone_folder(folder, folder, source_gis, target_gis)


def download_item(item, save_path=None):
    print(item.download(save_path=save_path))


def clone_operational_layers_to_new_webmap(source_webmap_obj, target_webmap_obj):
    layer_list = source_webmap_obj.layers

    for layer in layer_list:
        # Something is going wrong here cause the layers are a dict instead of actual layers
        target_webmap_obj.add_layer(layer)

    target_webmap_obj.update()
    return target_webmap_obj


def save_file(data, filename, file_type, save_folder=None):  # ~/Downloads (Work laptop)
    # if type == "geojson":
    #     data = geojson.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)

    if file_type == "json":
        data = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)

    with open(f"{save_folder}/{filename}.{file_type}", "w") as outfile:
        outfile.write(data)


def download_item_json(item, save_folder=None):

    save_folder = "../Data/JSON" if not save_folder else save_folder

    json_data = item.get_data()
    save_file(
        data=json_data, filename=item.id, file_type="json", save_folder=save_folder
    )


def save_file_locally(data, file_name, file_ext, folder_path=None):

    folder_path = "../../Data_Output/" if folder_path is None else folder_path

    with open(f"{folder_path}{file_name}.{file_ext}") as file:
        file.write(data)
        file.close()


def download_all_item_json_from_agol_folder(
    gis_obj, agol_folder, save_folder
):  # "~/Downloads" mac laptop

    if Path(save_folder).is_dir():
        items = get_funcs.get_items_from_folder(gis_obj=gis_obj, folder=agol_folder)
        for item in items:
            download_item_json(item, save_folder=save_folder)
    else:
        print(
            "I can't find that save_folder. Can you check your spelling pretty please?"
        )


def copy_over_map_bookmarks(webmap_item_1, webmap_item_2):
    webmap_1_obj = mapping.WebMap(webmap_item_1)
    webmap_1_bookmarks = webmap_1_obj.definition.bookmarks
    webmap_item_2_json = webmap_item_2.get_data()
    webmap_item_2_json["bookmarks"] = webmap_1_bookmarks
    item_properties = {"text": webmap_item_2_json}
    print(webmap_item_2.update(item_properties))


def clone_ags_to_agol(gis_obj, feature_layer_url):

    # Turn Feature Layer to a Feature Set
    feature_layer = features.FeatureLayer(url=feature_layer_url)
    feature_set = feature_layer.query()  # where="1=1", out_fields="*"

    # Turn FeatureSet into Feature
    feature_collection = features.FeatureCollection.from_featureset(feature_set)

    # Add the file to AGO and publish
    fc_item = gis_obj.content.add(
        item_properties={
            "type": "Feature Collection",
            "title": "MyFeautrelayerFromFC",
            "text": feature_collection._lyr_json,
        }
    )
    fc_item.publish(
        publish_parameters={
            "type": "Feature Collection",
            "name": "MyHostedFeautrelayerFromFC",
        }
    )


if __name__ == "__main__":
    # SOURCE_FOLDER = "Embedded_Scenarios_3x"
    TARGET_FOLDER = "_Cloned"

    REGRESSION_GIS = get_regression_devext_dbqa_gis()
    STORY_MAP_ITEM = REGRESSION_GIS.content.get("e42f5e2ccddf46ecae9eff62fc18dcdc")
    REGRESSION_GIS.content.clone_items(items=[STORY_MAP_ITEM], folder=TARGET_FOLDER)
