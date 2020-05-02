from arcgis import features, mapping

def get_dashboard_version(dashboard_json):
    try:
        if dashboard_json != {} and dashboard_json is not None:
            if dashboard_json != {'_ssl': False}: # Why is this happening?
                return dashboard_json['version']
        return None
    except: # Too general exception
        pass


def get_items_from_folder(gis_obj, folder, item_types=None) -> list: # folder=None returns the root folder
    folder_items = gis_obj.users.me.items(folder=folder)

    if item_types:
        folder_items = [item for item in folder_items if item.type in item_types]

    return folder_items

def get_items_from_folders(gis_obj, folders:list) -> list: # folder=None returns the root folder
    all_items = []
    for folder in folders:
        all_items += gis_obj.users.me.items(folder=folder)

    return all_items

def get_constructed_objects_from_items(items: list, gis) -> list:
    constructed_objects = []

    for item in items:
        try:
            if item.type == "Feature Service":
                if bool(item.url[-1].isdigit()):
                    feature_layer_obj = features.FeatureLayer(url=item.url, gis=gis)
                    feature_layer_obj = feature_layer_obj.properties # sometimes this triggers an error
                    constructed_objects.append(feature_layer_obj)

                feature_layer_collection = features.FeatureLayerCollection(url=item.url, gis=gis)
                constructed_objects.append(feature_layer_collection)

            elif item.type == "Web Map":
                constructed_objects.append(mapping.WebMap(webmapitem=item))

            elif item.type == "Dashboard":
                constructed_objects.append(item.get_data())
        except:
            pass

    return constructed_objects

def get_constructed_layers_from_from_webmap_obj(webmap_obj, gis) -> list:
    webmap_layers = webmap_obj.layers
    webmap_tables = webmap_obj.tables
    constructed_layers = []

    if webmap_layers:
        for layer in webmap_layers:
            if "url" in layer: # Clientside layers don't have a url
                try:
                    if bool(layer.url[-1].isdigit()):
                        layer = features.FeatureLayer(url=layer.url, gis=gis)
                        layer.properties # sometimes this triggers an attribute error. It is a sign the feature layer was not created sucessfully.
                    else:
                        layer = features.FeatureLayerCollection(url=layer.url, gis=gis)
                        layer.properties
                except:
                    pass
                
            if layer:
                constructed_layers.append(layer)

    if webmap_tables:
        for table in webmap_tables:
            if 'url' in table:
                try:
                    table = features.Table(url=table['url'], gis=gis)
                    if table:
                        constructed_layers.append(table)
                except:
                    pass

    return constructed_layers

def get_dashboard_item_data_sources(dashboard_json, gis)->list:
    data_source_item_ids = []
    if "widgets" in dashboard_json:
        for widget in dashboard_json["widgets"]:
            if widget["type"] == "mapWidget":
                if "mapId" in widget: # older schema
                    data_source_item_ids.append(widget["mapId"])
                else:
                    data_source_item_ids.append(widget["itemId"])

            elif "datasets" in widget:
                datasets = widget['datasets']
                for dataset in datasets:
                    if "dataSource" in dataset:
                        if "itemId" in dataset["dataSource"]:
                            layer_item_id = dataset["dataSource"]["itemId"]
                            data_source_item_ids.append(layer_item_id)

                        elif "dataSourceId" in dataset: #old schema
                            data_source_item_ids.append(dataset["dataSourceId"].split("#")[0]) # wtf

                    # if "headerPanel" in data and "selectors" in data["headerPanel"]:
                    #     for selector in data["headerPanel"]["selectors"]:
                    #         if "datasets" in selector:
                    #             if _process_dashboard_datasets(gis, selector["datasets"]):
                    #                 raise Exception

                    # if "leftPanel" in data and "selectors" in data["leftPanel"]: # rename to side panel?
                    #     for selector in data["leftPanel"]["selectors"]:
                    #         if "datasets" in selector:
                    #             if _process_dashboard_datasets(gis, selector["datasets"]):
                    #                 raise Exception

    item_objs = []
    for item_id in data_source_item_ids:
        try:
            item = gis.content.get(item_id)
            item_objs.append(item)
        except:
            pass

    return item_objs

import os
from pathlib import Path
import traceback
import pprint
import argparse
from arcgis.gis.server import Server
from arcgis import gis, mapping

def get_server_url(feature_service_url) -> str:
    """
    Always returns the full URL of a service. No sublayers.
    :param feature_service_url:
            https://sampleserver6.arcgisonline.com/arcgis/rest/services/CommunityAddressing/MapServer/0
    :type feature_service_url: string
    :return: A server url without a sublayer.
            https://sampleserver6.arcgisonline.com/arcgis/rest/services/CommunityAddressing/MapServer
    :rtype: string
    """

    if is_server_url(feature_service_url) is False:
        url_split = feature_service_url.split("/")
        server_url = '/'.join(url_split)[:-1]
        return server_url

    return feature_service_url

def get_projection_name(prj_factory_code) -> str:
    """
    :param prj_factory_code: Also called the spatial reference ID or SRID, this is a code that uniquely identifies a
                             spatial reference. It is also sometimes called a well known ID or WKid.
    :return: A string representation of a factory code. For example, the factory code, 3857 refers to a Pseudo
    Web Mercator spatial reference that is often used in AGOL. inputting 3857 into this function will return a
    human readable representation of the factory code.
    """
    sp_ref = osr.SpatialReference()
    sp_ref.ImportFromEPSG(prj_factory_code)
    return sp_ref.GetAttrValue("PROJCS")

def get_service_folder(feature_service_url, server) -> str:

    url_set = set(feature_service_url.split("/"))
    folder_set = set(server.content.folders)
    folder = url_set.intersection(folder_set)

    if folder:
        return folder
    else:
        return ''

def get_service_credential(org_url,
                           authentication_scheme,
                           username, password,
                           verify_cert=None,
                           key_file_path=None, cert_file_path=None,
                           client_id=None):

    standard_authentication_types = ["built_in", "ldap", "active_directory"]
    if authentication_scheme.name in standard_authentication_types:
        try:
            gis = GIS(org_url, username, password, verify_cert=verify_cert)
            return gis

        except Exception as e:
            traceback.print_exc()
            return False

    elif authentication_scheme.name == "iwa":
        try:
            return GIS(org_url, verify_cert=verify_cert)

        except Exception as e:
            traceback.print_exc()
            return False

    elif authentication_scheme.name == "pki":

        if key_file_path is None:
            print("No key file path provided")
            return

        try:
            return GIS(org_url, key_file_path=key_file_path, cert_file_path=cert_file_path, verify_cert=verify_cert)

        except Exception as e:
            traceback.print_exc()
            return False

    elif authentication_scheme.name == "o_auth":
        if client_id is None:
            print("No client id provided")
            return

        try:
            return GIS(org_url, client_id=client_id, verify_cert=verify_cert)

        except Exception as e:
            traceback.print_exc()
            return False

    elif authentication_scheme.name == "server":
        try:
            return Server(url=org_url, username=username, password=password, verify_cert=verify_cert)

        except Exception as e:
            traceback.print_exc()
            return False

def get_feature_from_fs_url(feature_service_url, gis=None):

    if is_server_url(feature_service_url) is True:
        return FeatureLayerCollection(feature_service_url, gis=gis)

    else:
        return FeatureLayer(feature_service_url, gis=gis)

def get_folder_names(gis):
    return gis.users.me.folders

def get_items_from_folders(gis_obj, folders:list, item_types=None) -> list: # folder=None returns items in the root folder
    all_items = []
    for folder in folders:
        folder_items = gis_obj.users.me.items(folder=folder)
        all_items += get_items_from_folder(gis_obj, folder, item_types)

    return all_items

def get_items_from_folder(gis_obj, folder, item_types=None) -> list: # folder=None returns items in the root folder
    folder_items = gis_obj.users.me.items(folder=folder)

    if item_types:
        folder_items = [item for item in folder_items if item.type in item_types]

    return folder_items

def get_layer_attachmets(layer):
    attachments = layer.attachments.search(where='1=1') # this returns an unformatted dict
    pretty_json = convert_stuff.raw_json_to_pretty_json(attachments)
    return pretty_json

def get_feature_layer_extent(feature_layer, out_sr):
    '''
    4326 = WGS84
    3857 = Web Merc
    '''
    return feature_layer.query(return_extent_only=True, out_sr=out_sr)['extent']

def get_feature_count_from_feature_layer(feature_layer):
    return feature_layer.query(return_count_only=True)

def get_files_in_directory(directory=None, extension=None) -> Path:
    if directory is None: # Loop current directory if one isn't provided
        directory = os.getcwd()

    # combine current directory with provided directory
    for path, dirs, files in os.walk(directory):
        if extension: # Only get files with a certain extension if one is specified
            return [Path(os.path.join(path,f)) for f in files if f.endswith(extension)]
        else:
            return [Path(os.path.join(path,f)) for f in files]
    
def get_item_json(item):
    return item.get_data()


def export_agol_item(item, export_title, export_format):
    """[Export an agol item to various formats]
    
    Args:
        item ([type]): [The item to be exported]
        export_title ([type]): [The title of the exported item]
        export_format ([type]): [The format to export the data to.
                                 Allowed types: ‘Shapefile’, ‘CSV’,
                                 ‘File Geodatabase’, ‘Feature Collection’,
                                 ‘GeoJson’, ‘Scene Package’, ‘KML’]
    """

    return item.export(title=export_title, export_format=export_format)


def get_layer_capabilities_from_webmap(id, gis_obj):
    item = gis.Item(itemid=id, gis=gis_obj)
    webmap_obj = mapping.WebMap(webmapitem=item)
    print(webmap_obj)

if __name__ == "__main__":
    # Get all of the commandline arguments
    parser = argparse.ArgumentParser("")
    parser.add_argument('-org', dest='org', help="", required=True)
    parser.add_argument('-username', dest='username', help="The username of the portal", required=True)
    parser.add_argument('-password', dest='password', help="The associated password", required=True)
    args = parser.parse_args()

    GIS_USER = gis.GIS(url=args.org, username=args.username, password=args.password, verify_cert=False)


    #get_layer_capabilities_from_webmap(id="89c21e471c9543d3930f74e33ac3a3e1", gis_obj=GIS_USER)

    item = gis.Item(gis=GIS_USER,itemid='ebe035b2428a4d9fbda1be876443cafa')
    data = item.get_data()
    pprint.pprint(data)
    #print(get_files_in_folder("~/Documents/Data/MERGE_ME_COPY", full_path=None, file_type=".shp"))
    #print (convert_stuff.raw_json_to_pretty_json(Item.get_data()))



    #### Download item to folder ####
    # feature_layer = features.FeatureLayer(gis=GIS_USER, url="")
    # df = feature_layer.query(query="1=1", as_df=True)
    # csv = convert_stuff.pandas_df_to_csv(df, "ChicagoCr.csv", "~/Downloads")

    ### Download items from Folder ####
    # items = get_items_from_folder(GIS_USER, folder=SOURCE_FOLDER, item_type="File Geodatabase")
    # for item in items:
    #     try:
    #         item.download(save_path="~/Documents/Data/Sanity_GDBs")
    #     except Exception as e:
    #         continue

    #### Mac ####
    #file_objects = get_files_in_directory("~/Downloads", extension="json")

    #### Windows ###
    # file_objects = get_files_in_directory("~/Downloads", extension="txt")
    # print (file_objects)
    # feature_layer = features.FeatureLayer(url="url")
    # print (feature_layer)



    #### Get Dashboard JSON and Save! ####
    # ITEM = GIS_USER.content.get(itemid="c70ab9d2f9b84806aaa3ff4ac73386f9")
    # a = ITEM.get_data(try_json=False)
    # with open("~/Documents/Data/Dashboards/Dashboard_with_map.json", "w") as writer_obj:
    #     writer_obj.write(a)