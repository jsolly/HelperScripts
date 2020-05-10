from arcgis import features, gis
from GitHub.HelperScripts import convert_funcs
import os
from pathlib import Path
import traceback
import pprint
import argparse
from arcgis.gis.server import Server
from arcgis import gis, mapping


def get_dashboard_version(dashboard_json):
    try:
        if dashboard_json != {} and dashboard_json is not None:
            if dashboard_json != {"_ssl": False}:  # Why is this happening?
                return dashboard_json["version"]
        return None
    except:  # Too general exception
        pass


def get_items_from_folder(
    gis_obj, folder, item_types=None
) -> list:  # folder=None returns the root folder
    folder_items = gis_obj.users.me.items(folder=folder)

    if item_types:
        folder_items = [item for item in folder_items if item.type in item_types]

    return folder_items


def get_items_from_folders(
    gis_obj, folders: list
) -> list:  # folder=None returns the root folder
    all_items = []
    for folder in folders:
        all_items += gis_obj.users.me.items(folder=folder)

    return all_items


def get_constructed_objects_from_items(items: list, gis_obj) -> list:
    constructed_objects = []

    for item in items:
        try:
            if item.type == "Feature Service":
                if bool(item.url[-1].isdigit()):
                    feature_layer_obj = features.FeatureLayer(url=item.url, gis=gis_obj)
                    feature_layer_obj = (
                        feature_layer_obj.properties
                    )  # sometimes this triggers an error
                    constructed_objects.append(feature_layer_obj)

                feature_layer_collection = features.FeatureLayerCollection(
                    url=item.url, gis=gis_obj
                )
                constructed_objects.append(feature_layer_collection)

            elif item.type == "Web Map":
                constructed_objects.append(mapping.WebMap(webmapitem=item))

            elif item.type == "Dashboard":
                constructed_objects.append(item.get_data())
        except:
            pass

    return constructed_objects


def get_constructed_layers_from_from_webmap_obj(webmap_obj, gis_obj) -> list:
    webmap_layers = webmap_obj.layers
    webmap_tables = webmap_obj.tables
    constructed_layers = []

    if webmap_layers:
        for layer in webmap_layers:
            if "url" in layer:  # Clientside layers don't have a url
                try:
                    if bool(layer.url[-1].isdigit()):
                        layer = features.FeatureLayer(url=layer.url, gis=gis_obj)
                        # sometimes accessing properties triggers an attribute error.
                        layer.properties
                    else:
                        layer = features.FeatureLayerCollection(
                            url=layer.url, gis=gis_obj
                        )
                        layer.properties
                except:
                    pass

            if layer:
                constructed_layers.append(layer)

    if webmap_tables:
        for table in webmap_tables:
            if "url" in table:
                try:
                    table = features.Table(url=table["url"], gis=gis_obj)
                    if table:
                        constructed_layers.append(table)
                except:
                    pass

    return constructed_layers


def get_dashboard_item_data_sources(dashboard_json, gis) -> list:
    data_source_item_ids = []
    if "widgets" in dashboard_json:
        for widget in dashboard_json["widgets"]:
            if widget["type"] == "mapWidget":
                if "mapId" in widget:  # older schema
                    data_source_item_ids.append(widget["mapId"])
                else:
                    data_source_item_ids.append(widget["itemId"])

            elif "datasets" in widget:
                datasets = widget["datasets"]
                for dataset in datasets:
                    if "dataSource" in dataset:
                        if "itemId" in dataset["dataSource"]:
                            layer_item_id = dataset["dataSource"]["itemId"]
                            data_source_item_ids.append(layer_item_id)

                        elif "dataSourceId" in dataset:  # old schema
                            data_source_item_ids.append(
                                dataset["dataSourceId"].split("#")[0]
                            )  # wtf

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


def get_service_folder(feature_service_url, server):

    url_set = set(feature_service_url.split("/"))
    folder_set = set(server.content.folders)
    folder = url_set.intersection(folder_set)

    if folder:
        return folder
    else:
        return ""


def get_service_credential(
    org_url,
    authentication_scheme,
    username,
    password,
    verify_cert=None,
    key_file_path=None,
    cert_file_path=None,
    client_id=None,
):

    standard_authentication_types = ["built_in", "ldap", "active_directory"]
    if authentication_scheme.name in standard_authentication_types:
        try:
            return gis.GIS(org_url, username, password, verify_cert=verify_cert)

        except Exception as e:
            traceback.print_exc()
            return False

    elif authentication_scheme.name == "iwa":
        try:
            return gis.GIS(org_url, verify_cert=verify_cert)

        except Exception as e:
            traceback.print_exc()
            return False

    elif authentication_scheme.name == "pki":

        if key_file_path is None:
            print("No key file path provided")
            return

        try:
            return gis.GIS(
                org_url,
                key_file_path=key_file_path,
                cert_file_path=cert_file_path,
                verify_cert=verify_cert,
            )

        except Exception as e:
            traceback.print_exc()
            return False

    elif authentication_scheme.name == "o_auth":
        if client_id is None:
            print("No client id provided")
            return

        try:
            return gis.GIS(org_url, client_id=client_id, verify_cert=verify_cert)

        except Exception as e:
            traceback.print_exc()
            return False

    elif authentication_scheme.name == "server":
        try:
            return Server(
                url=org_url,
                username=username,
                password=password,
                verify_cert=verify_cert,
            )

        except Exception as e:
            traceback.print_exc()
            return False


# Broken
# def get_feature_from_fs_url(feature_service_url, gis_obj=None):
#
#     if is_server_url(feature_service_url) is True:
#         return FeatureLayerCollection(feature_service_url, gis=gis_obj)
#
#     else:
#         return FeatureLayer(feature_service_url, gis=gis_obj)


def get_folder_names(gis):
    return gis.users.me.folders


def get_items_from_folders(
    gis_obj, folders: list, item_types=None
) -> list:  # folder=None returns items in the root folder
    all_items = []
    for folder in folders:
        all_items += get_items_from_folder(gis_obj, folder, item_types)

    return all_items


def get_items_from_folder(
    gis_obj, folder, item_types=None
) -> list:  # folder=None returns items in the root folder
    folder_items = gis_obj.users.me.items(folder=folder)

    if item_types:
        folder_items = [item for item in folder_items if item.type in item_types]

    return folder_items


def get_layer_attachmets(layer):  # Add return type?
    attachments = layer.attachments.search(
        where="1=1"
    )  # this returns an unformatted dict
    return attachments


def get_feature_layer_extent(feature_layer, out_sr):
    """
    4326 = WGS84
    3857 = Web Merc
    """
    return feature_layer.query(return_extent_only=True, out_sr=out_sr)["extent"]


def get_feature_count_from_feature_layer(feature_layer):
    return feature_layer.query(return_count_only=True)


def get_files_in_directory(directory=None, extension=None):
    if directory is None:  # Loop current directory if one isn't provided
        directory = os.getcwd()

    # combine current directory with provided directory
    for path, dirs, files in os.walk(directory):
        if extension:  # Only get files with a certain extension if one is specified
            return [Path(os.path.join(path, f)) for f in files if f.endswith(extension)]
        else:
            return [Path(os.path.join(path, f)) for f in files]


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


def get_layer_capabilities_from_webmap(itemid, gis_obj):
    item = gis.Item(itemid=itemid, gis=gis_obj)
    webmap_obj = mapping.WebMap(webmapitem=item)
    print(webmap_obj)


if __name__ == "__main__":
    print("I am running from __main___")
