import convert_stuff
import get_stuff
import edit_stuff
import create_stuff
import time
import os
import subprocess
import numpy
import pandas
from arcgis import gis, mapping, features
from arcgis.apps import storymap
from pathlib import Path
import requests
import traceback
import argparse
import my_secrets as secrets
from pathlib import Path
HOME = str(Path.home())

def add_and_publish_file(gis_obj, file_path, file_type=None, agol_folder=None, title=None) -> gis.Item:

    if not title:
        path_obj = Path(file_path)
        title = path_obj.stem

    item_prop = {'title': title,
                 'type': file_type}
    try:
        item = gis_obj.content.add(item_properties=item_prop, data=file_path, folder=agol_folder)
        if file_type != 'Dashboard':
            item = item.publish()
        return item
        
    except Exception as e:
        traceback.print_exc()


def publish_items(items: list):
    for item in items:
        try:
            item.publish()
        except Exception as e:
            traceback.print_exc()


def publish_items_in_folder(gis_obj, agol_folder):
    items = get_stuff.get_items_from_folders(gis_obj=gis_obj, folders=[agol_folder])
    publish_items(items)

def REST_publish_item(gis_obj, parameters:dict):
    publish_url = f"https://{secrets.AGOL_DEV_REST_BASE_URL}/sharing/rest/content/users/{secrets.AGOL_DBQA_REGRESSION_USERNAME}/publish"
    response = requests.post(publish_url, data=parameters)
    print(response.text)

def create_objectID_string(number_of_objects):
    return ','.join([str(x) for x in range(number_of_objects)])

def merge_shape_files(shape_file_folder, merged_name="Merged.shp"):
    shapefiles = get_stuff.get_files_in_folder(folder_path=shape_file_folder, file_type=".shp")
    shapefiles_comma_seperated_string = convert_stuff.list_to_string(shapefiles)
    
    os.chdir(shape_file_folder)
    args = [f"ogrmerge.py, -single, -o, {merged_name}, {shapefiles_comma_seperated_string}"]
    subprocess.call(args)

def create_webmaps_from_feature_layer_items(layer_items, agol_folder):
    for layer_item in layer_items:
        create_webmap_from_feature_layer_item(layer_item, agol_folder)

def create_webmap_from_feature_layer_item(layer_item, agol_folder=None, title=None):

    title = layer_item.title if title is None else title

    webmap_item_properties = {"title":title, "tags":layer_item.id, "snippet":"This is a snippet"}
    webmap = mapping.WebMap()
    try:
        webmap.add_layer(layer_item)

    except TypeError:
        print(f"Could not add layer {title} to webmap")

    webmap_item = webmap.save(item_properties=webmap_item_properties, folder=agol_folder)
    return webmap_item

def create_webmap_from_feature_layer(feature_layer, agol_folder):
    webmap_item_properties = {"title":"Sample_Webmap", "tags":"DashboardQA", "snippet":"This is a snippet"}
    webmap = mapping.WebMap()
    try:
        webmap.add_layer(feature_layer)
    except TypeError:
        print(f"Could not add feature layer with url {feature_layer.url} to webmap")

    webmap_item = webmap.save(item_properties=webmap_item_properties, folder=agol_folder)
    return webmap_item


def create_webmap_with_missing_layer_from_file(gis_obj, file_type, file_path, agol_folder=None):
    layer_item = create_stuff.add_and_publish_file(gis_obj=gis_obj, file_path=file_path, file_type=file_type, folder=agol_folder)
    webmap_item_properties = {"title":layer_item.title, "tags":"DashboardQA", "snippet":"This is a snippet"}
    webmap = mapping.WebMap()
    try:
        webmap.add_layer(layer_item)
    except TypeError:
        traceback.print_exc()
        print(f"Could not add layer {layer_item.title} to webmap")

    webmap.save(item_properties=webmap_item_properties, folder=agol_folder) # returns webmap item
    layer_item.delete()

def create_webmap_from_public_layer(agol_folder=None):
    PUBLIC_LAYER = features.FeatureLayer(url="http://sampleserver6.arcgisonline.com/arcgis/rest/services/CommercialDamageAssessment/FeatureServer/0")
    WEBMAP = create_webmap_from_feature_layer(PUBLIC_LAYER, folder=agol_folder)
    return WEBMAP

def create_dashboard(gis_obj, dashboard_json_path, file_type='Dashboard'):
    add_and_publish_file(gis_obj, dashboard_json_path, file_type)

def create_storymap_journal_with_dashboard_url(dashboard_url):
    new_journal = storymap.JournalStoryMap()
    #new_journal.add(title="Dashboard", url_or_item=dashboard_url)
    new_journal.save(title="Sample Journal", tags="DashboardQA")


def create_folder_in_agol(gis_obj, folder_name):
    try:
        gis_obj.content.create_folder(folder=folder_name)
    except Exception as e: # If the folder is already there
        traceback.print_exc()

def create_group_in_agol(gis_obj, group_name):
    try:
        gis_obj.groups.create(title=group_name, tags="DashboardQA")
    except Exception as e: # If the group is already there
        traceback.print_exc()

if __name__ == "__main__":
    SOURCE_AGOL_FOLDER = "_Generic_Services"
    DESTINATION_AGOL_FOLDER = "Vis_Details"
    FILE_PATH = f"{HOME}/Downloads/RedlandsCensusBlocksNearEsri.zip"
    
    add_and_publish_file(secrets.REGRESSION_DEVEXT_DBQA_GIS,
                         file_path=FILE_PATH,
                         file_type="File Geodatabase",
                         agol_folder=DESTINATION_AGOL_FOLDER,
                         title=None)

    ## Add and publish a dashboard JSONS
    # FILES = get_stuff.get_files_in_directory(LOCAL_DIRECTORY)
    # for FILE in FILES:
    #     add_and_publish_file(gis_obj=GIS_USER, file_path=FILE._str, file_type='Dashboard', agol_folder='maxPaginationRecords')

