import os
import json
from pathlib import PurePosixPath
import argparse
from pyproj import transform
from arcgis import gis, features
from GitHub.HelperScripts import get_funcs


def update_item_data(item):
    # item_properties = {"title": "I am a changed title"}
    print(item.update(data="d9e8b46c430e4a669e246b29fd341f13.json"))


# def add_type_keywords_to_item(item, type_keywords_to_be_added):
#     final_type_keywords_diff = set(type_keywords_to_be_added).difference(
#         set(item["type_keywords"])
#     )
#     final_type_keywords_string = "".join(
#         item["type_keywords"], final_type_keywords_diff
#     )
#     item_properties = {"type_keywords": final_type_keywords_string}
#     print(
#         "I am adding type_keywords '{}' from item {}".format(
#             type_keywords_to_be_added, item.title
#         )
#     )
#     item.update(item_properties=item_properties)


#
# def remove_type_keywords_from_item(item, type_keywords_to_be_removed):
#     final_type_keywords_string = "".join(final_type_keywords_diff)
#     item_properties = {"type_keywords": final_type_keywords_string}
#     print(
#         "I am removing type_keywords '{}' from item {}".format(
#             type_keywords_to_be_removed, item.title
#         )
#     )
#     item.update(item_properties=item_properties)


# def toggle_save_as_on_item(item):
#     if "useOnly" not in item["type_keywords"]:
#         add_type_keywords_to_item(item, ["useOnly"])
#     else:
#         remove_type_keywords_from_item(item, ["useOnly"])


def share_all_items_in_agol_account(
    gis_obj, org=False, everyone=False, groups=None, ignore_folder=None
):  # might have broken this
    folders = gis_obj.users.me.folders
    for folder in folders:
        items = gis_obj.users.me.items(folder=folder)

        if folder == ignore_folder:
            for item in items:
                print(item.share(org=False))

        else:
            for item in items:
                print(item.share(org=org, everyone=everyone, groups=groups))


def share_all_items_in_folder(gis_obj, folder, org=False, everyone=False, groups=None):
    items = gis_obj.users.me.items(folder=folder)
    for item in items:
        print(item.share(org=org, everyone=everyone, groups=groups))


def add_file_extensions(folder_path, extension):
    files = get_funcs.get_files_in_directory(directory=folder_path, extension=extension)
    for file in files:
        file_stem = PurePosixPath(file).stem
        os.rename(file, f"{file_stem}.{extension}")


# def add_feature_layer_to_webmap_json(feature_layer, webmap_json):  # Broken?
#     """
#     Adds a layer to an unpublished webmap json
#     :param feature_layer: An Esri layer object that will be added to a webmap
#     :type feature_layer: An Esri layer object
#     :param webmap_json: A json representation of a webmap. This webmap can have 0 - > n operational layers.
#                         This function will add one more operational layer.
#     :type webmap_json: A json file
#     :return: A new python dictionary is returned. This dictionary is exactly the same as the input except that it has
#              one more operational layer.
#     """
#     # I might have broke this
#
#     feature_layer_dict = {
#         "title": feature_layer.properties["name"],
#         "url": feature_layer.url,
#     }
#     # Add the layer as an operational layer
#     webmap_json["operationalLayers"].update(feature_layer_dict)
#
#     return webmap_json


def add_json_layer_to_webmap_json(json_layer, webmap_json) -> json:
    webmap_json["operationalLayers"].update(json_layer)
    return webmap_json


def overwrite_feature_service(feature_service_url, source_data):
    feature_layer_collection = features.FeatureLayerCollection(url=feature_service_url)
    print(feature_layer_collection.manager.overwrite(source_data))


def delete_items_from_folder(gis_obj, agol_folder):
    items = gis_obj.users.me.items(folder=agol_folder)
    for item in items:
        item.delete()
    return


def delete_unzipped_shp_files_from_directory(folder):

    shapefile_file_extensions = (
        ".cpg",
        ".dbf",
        ".prj",
        ".sbn",
        ".sbx",
        ".shp",
        ".xml",
        ".shx",
    )
    for root, dirs, files in os.walk(folder):
        for file in files:
            filename, extension = os.path.splitext(file)
            if extension in shapefile_file_extensions:
                os.remove(os.path.join(root, file))
    return


def df_to_agol(gis_obj, df, title):
    feature_collection = gis_obj.content.import_data(df=df, title=title)
    item_properties = {
        "title": title,
        "text": json.dumps(
            {"featureCollection": {"layers": [dict(feature_collection.layer)]}}
        ),
        "type": "Feature Collection",
    }
    gis_obj.content.add(item_properties=item_properties).publish()


def convert_projection(coordinate_tuple, in_prj, out_prj):
    """[Converts coordinate pairs to a different coordinate system]
    
    Args:
        coordinate_tuple ([tuple]): [example - > (lat, long) - > (10.25, 28.49)]
        in_prj ([string]): [The projection coming in...Use format 'epsg:<srid>']
        Because I like you.... web_mercator (3857), WGS84 (4326)
        out_prj ([string]): [The projection going out]
    
    Returns:
        [tuple]: [description]
    """
    x1, y1 = coordinate_tuple
    x1, y1 = transform(in_prj, out_prj, x1, y1)
    return x1, y1


#
# def add_prj_to_shapefiles(shapefile_folder):
#     shapefiles = get_funcs.get_files_in_directory(
#         folder_path=shapefile_folder, file_type=".shp"
#     )
#     shapefiles_comma_seperated_string = convert_funcs.list_to_string(shapefiles)


def remove_features_from_feature_layer(feature_layer_obj, number_of_features_to_remove):
    feature_set_copy = feature_layer_obj.query()
    feature_set_features = feature_set_copy._features

    features_to_remove = feature_set_features[:number_of_features_to_remove]
    feature_set_copy._features = features_to_remove

    feature_layer_obj.edit_features(deletes=feature_set_copy)

    # Write a function that leverages my prj folder


def change_webmap_in_local_dashboard_json(dashboard_json_path, new_webmap_id):
    with open(dashboard_json_path) as read_obj:
        with open(f"{dashboard_json_path}_MODIFIED", "w") as write_obj:
            dashboard_dict = json.load(read_obj)
            dashboard_dict["widgets"][0]["itemId"] = new_webmap_id
            write_obj.write(json.dumps(dashboard_dict))

    # Open dashboard json file
    # replace webmap item id
    # save Dashboard JSON


if __name__ == "__main__":
    # Get all of the commandline arguments
    parser = argparse.ArgumentParser("")
    parser.add_argument("-org", dest="org", help="", required=True)
    parser.add_argument(
        "-username", dest="username", help="The username of the portal", required=True
    )
    parser.add_argument(
        "-password", dest="password", help="The associated password", required=True
    )
    args = parser.parse_args()

    GIS_USER = gis.GIS(
        url=args.org, username=args.username, password=args.password, verify_cert=False
    )

    feature_layer = features.FeatureLayer(
        url="https://servicesdev.arcgis.com/zImu9NfARSUcVsy1/ArcGIS/rest/services/5_Features/FeatureServer/0",
        gis=GIS_USER,
    )

    remove_features_from_feature_layer(feature_layer, 7)

    # feature_layer = features.FeatureLayer(gis=GIS_USER_1, url='')
    # delete_all_features(feature_layer=feature_layer)

    # add_file_extensions(folder_path="~/Downloads", extension="json")

    # Delete an Item
    # item = gis.Item(GIS_USER, "")
    # item.delete()

    # layer = features.FeatureLayer(url="", gis=GIS_USER)
    # print(layer.delete_features(where="unitname is null"))

    # parameters = {'where':'1=1', 'returnExtentOnly':'true', 'f':'pjson'}
    # query_url = ""
    # response = requests.get(query_url, params=parameters)
    # print(response.text)

    # parameters = {"where":"UnitName=Null"}
    # delete_features_url = ""
    # response = requests.post(delete_features_url, params=parameters)
    # print(response)

    # import random
    # import time
    # import names
    #
    #
    # def add_feature_to_feature_layer(feature_layer):
    #     feature_set = feature_layer.query()
    #
    #     feature = random.choice(feature_set.features)
    #     feature_set._features = [feature]
    #
    #     feature_layer.edit_features(adds=feature_set)
    #
    #
    # def remove_feature_from_feature_layer(feature_layer):
    #     feature_set = feature_layer.query()
    #
    #     feature_to_delete = random.choice(feature_set.features)
    #     feature_set._features = [feature_to_delete]
    #
    #     feature_layer.edit_features(deletes=feature_set)
    #
    #
    # def modify_numeric_value(feature_layer):
    #     feature_set = feature_layer.query()
    #
    #     modified_features = []
    #     for feature in feature_set.features:
    #         feature = random.choice(feature_set.features)
    #
    #         feature.attributes["int_field"] = random.randint(0, 100)
    #         modified_features.append(feature)
    #
    #     feature_set._features = modified_features
    #
    #     feature_layer.edit_features(updates=feature_set)
    #
    #
    # def modify_string_value(feature_layer):
    #     feature_set = feature_layer.query()
    #
    #     modified_features = []
    #     for feature in feature_set.features:
    #         feature = random.choice(feature_set.features)
    #
    #         feature.attributes["namefield"] = names.get_full_name()
    #         modified_features.append(feature)
    #     feature_set._features = modified_features
    #
    #     feature_layer.edit_features(updates=feature_set)
