import os
import subprocess
from arcgis import gis, mapping, features
import requests
import traceback
from pathlib import Path
from GitHub.HelperScripts import convert_funcs, get_funcs
from arcgis.apps.storymap import JournalStoryMap
from other.my_secrets import get_regression_devext_dbqa_gis, AGOL_DICT

HOME = str(Path.home())

REGRESSION_GIS = get_regression_devext_dbqa_gis()
NICKEL_BUILDER = AGOL_DICT["NICKEL_BUILDER_HOST_NAME"]
PROD_URL_PARAM = AGOL_DICT["3X_URL_PARAM"]
BETA_URL_PARAM = AGOL_DICT["4X_URL_PARAM"]


def create_storymap_from_dashboards_using_pr(dashboard_items, pr_num, dashboard_type):
    storymap = JournalStoryMap(gis=REGRESSION_GIS)
    public_webmap = REGRESSION_GIS.content.get("c3d9f73238e34354a86239c4732c0524")
    storymap.add(
        title="Public Webmap", content="Public Webmap", url_or_item=public_webmap,
    )
    if dashboard_type == "3x":
        for dashboard_item in dashboard_items:
            storymap.add(
                title=dashboard_item.title,
                content=dashboard_item.title,
                url_or_item=f"{NICKEL_BUILDER}/PR-{pr_num}/#/{dashboard_item.id}{PROD_URL_PARAM}",
            )
    else:
        for dashboard_item in dashboard_items:
            storymap.add(
                title=dashboard_item.title,
                url_or_item=f"{NICKEL_BUILDER}/PR-{pr_num}/dashboards/{dashboard_item.id}{BETA_URL_PARAM}",
            )
    storymap.save(title="Dashboard Embed Scenarios")


def add_and_publish_file(
    gis_obj, file_path, file_type=None, agol_folder=None, title=None
) -> gis.Item:

    title = Path(file_path).stem if not title else title

    item_prop = {"title": title, "type": file_type}
    item = gis_obj.content.add(
        item_properties=item_prop, data=file_path, folder=agol_folder
    )
    if file_type != "Dashboard":
        item = item.publish()
    return item


def publish_items(items: list):
    for item in items:
        item.publish()


def publish_items_in_folder(gis_obj, agol_folder):
    items = get_funcs.get_items_from_folders(gis_obj=gis_obj, folders=[agol_folder])
    publish_items(items)


def rest_publish_item(parameters: dict):
    publish_url = f"https://{AGOL_DICT['AGOL_DEV_REST_BASE_URL']}/sharing/rest/content/users/\
        {AGOL_DICT['AGOL_DBQA_REGRESSION_USERNAME']}/publish"
    response = requests.post(publish_url, data=parameters)
    print(response.text)


def create_object_id_string(number_of_objects):
    return ",".join([str(x) for x in range(number_of_objects)])


def merge_shape_files(shape_file_folder, merged_name="Merged.shp"):
    shapefiles = get_funcs.get_files_in_directory(
        directory=shape_file_folder, extension=".shp"
    )
    shapefiles_comma_seperated_string = convert_funcs.list_to_string(shapefiles)

    os.chdir(shape_file_folder)
    args = [
        f"ogrmerge.py, -single, -o, {merged_name}, {shapefiles_comma_seperated_string}"
    ]
    subprocess.call(args)


def create_webmaps_from_feature_layer_items(layer_items, agol_folder):
    for layer_item in layer_items:
        create_webmap_from_feature_layer_item(layer_item, agol_folder)


def create_webmap_from_feature_layer_item(layer_item, agol_folder=None, title=None):

    title = layer_item.title if title is None else title

    webmap_item_properties = {
        "title": title,
        "tags": layer_item.id,
        "snippet": "This is a snippet",
    }
    webmap = mapping.WebMap()
    try:
        webmap.add_layer(layer_item)

    except TypeError:
        print(f"Could not add layer {title} to webmap")

    webmap_item = webmap.save(
        item_properties=webmap_item_properties, folder=agol_folder
    )
    return webmap_item


def create_webmap_from_feature_layer(feature_layer, agol_folder):
    webmap_item_properties = {
        "title": "Sample_Webmap",
        "tags": "DashboardQA",
        "snippet": "This is a snippet",
    }
    webmap = mapping.WebMap()
    try:
        webmap.add_layer(feature_layer)
    except TypeError:
        print(f"Could not add feature layer with url {feature_layer.url} to webmap")

    webmap_item = webmap.save(
        item_properties=webmap_item_properties, folder=agol_folder
    )
    return webmap_item


def create_webmap_with_missing_layer_from_file(
    gis_obj, file_type, file_path, agol_folder=None
):
    layer_item = add_and_publish_file(
        gis_obj=gis_obj,
        file_path=file_path,
        file_type=file_type,
        agol_folder=agol_folder,
    )
    webmap_item_properties = {
        "title": layer_item.title,
        "tags": "DashboardQA",
        "snippet": "This is a snippet",
    }
    webmap = mapping.WebMap()
    try:
        webmap.add_layer(layer_item)
    except TypeError:
        traceback.print_exc()
        print(f"Could not add layer {layer_item.title} to webmap")

    webmap.save(
        item_properties=webmap_item_properties, folder=agol_folder
    )  # returns webmap item
    layer_item.delete()


def create_webmap_from_public_layer(agol_folder=None):
    public_layer = features.FeatureLayer(
        url="http://sampleserver6.arcgisonline.com/arcgis/rest/services/CommercialDamageAssessment/FeatureServer/0"
    )
    webmap = create_webmap_from_feature_layer(public_layer, agol_folder=agol_folder)
    return webmap


def create_dashboard(gis_obj, dashboard_json_path, file_type="Dashboard"):
    add_and_publish_file(gis_obj, dashboard_json_path, file_type)


def create_group_in_agol(gis_obj, group_name):
    gis_obj.groups.create(title=group_name, tags="DashboardQA")


if __name__ == "__main__":
    SOURCE_AGOL_FOLDER = "_Generic_Services"
    DESTINATION_AGOL_FOLDER = "Vis_Details"
    FILE_PATH = f"{HOME}/Downloads/RedlandsCensusBlocksNearEsri.zip"

    add_and_publish_file(
        AGOL_DICT["REGRESSION_DEVEXT_DBQA_GIS"],
        file_path=FILE_PATH,
        file_type="File Geodatabase",
        agol_folder=DESTINATION_AGOL_FOLDER,
    )

    # Add and publish a dashboard JSONS
    # FILES = get_funcs.get_files_in_directory(LOCAL_DIRECTORY)
    # for FILE in FILES:
    # add_and_publish_file(
    #     gis_obj=GIS_USER,
    #     file_path=FILE._str,
    #     file_type="Dashboard",
    #     agol_folder="maxPaginationRecords",
    # )
