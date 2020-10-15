from arcgis import features
import os
import re
from pathlib import Path
from arcgis.gis.server import Server
from arcgis import gis, mapping
from urllib.parse import urlparse
import time
import subprocess
from json.decoder import JSONDecodeError
from other.my_secrets import MySecrets


def get_all_items_in_org(gis_obj, item_type="Dashboard"):
    return gis_obj.content.advanced_search(
        f"type: {item_type} AND orgid:{gis_obj.properties.id}", max_items=5000
    )["results"]


def get_group_id_from_group_name(gis_obj, group_name):
    top_result = gis_obj.groups.search(query=group_name)[0]
    return top_result.id


def get_dashboard_ids_with_webmap(gis_user, webmap_id, orgid):  # This needs work
    dashboards = gis_user.content.advanced_search(
        f'type: "Dashboard" AND orgid:{orgid}', max_items=2000
    )["results"]
    dashboard_ids_dict = {}
    for dashboard_item in dashboards:
        dashboard_dict = dashboard_item.get_data()
        if "widgets" in dashboard_dict:
            for widget in dashboard_dict["widgets"]:
                if widget["type"] == "mapWidget":
                    if widget["itemId"] == webmap_id:
                        dashboard_ids_dict[dashboard_item.owner] = dashboard_item.id
                        break  # No need to find it multiple times

    return dashboard_ids_dict


def get_links_from_string(string) -> list:
    url_pattern = re.compile(
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    urls = url_pattern.findall(string)
    for index, url in enumerate(urls):
        matches = [")", ",", "'"]
        if any(
            x in url for x in matches
        ):  # This logic could bite me later. Pretty fragile.
            urls[index] = url.replace(")", "").replace(",", "").replace("'", "")
            if urls[index][-1] == ".":
                urls[index] = urls[index][:-1]
    return urls


def get_item_ids_from_string(string):
    item_id_pattern = re.compile("[0-9a-f]{32}")
    item_ids = item_id_pattern.findall(string)
    return item_ids


def get_item_from_item_id(item_id, gis_objs: list):

    for gis_obj in gis_objs:
        try:
            item = gis_obj.content.get(item_id)
            if item:
                return item
        except ConnectionError:
            # Sometimes happens. Not sure why
            continue

        except Exception as e:
            if "Item does not exist" in e.args[0]:
                continue

            if "do not have permissions" in e.args[0]:
                continue

            else:
                raise Exception("I have never seen this error before")

    return False


def get_item_host_name(item_obj):
    item_url = item_obj.homepage
    host_name = urlparse(item_url).hostname
    return host_name


def get_items_from_group(gis_obj, group_id, item_types=None):
    group_items = gis_obj.groups.get(group_id).content()  # max_items=1000

    if item_types:
        filtered_items = [item for item in group_items if item.type in item_types]
        return filtered_items

    return group_items


def get_func_run_time(func, *args):
    t1 = time.perf_counter_ns()
    func(*args)
    t2 = time.perf_counter_ns()
    return t2 - t1


def get_file_line_count_python(file_path) -> int:
    with open(file_path) as my_file:
        return sum(1 for _ in my_file)


def get_file_line_count_bash(file_path):
    line_count = subprocess.run(
        [f"cat {file_path} | wc -l"], capture_output=True, text=True, shell=True
    )
    return int(line_count.stdout.strip())


def get_item_id_from_dashboard_url(dashboard_url) -> str:
    item_id_pattern = re.compile("[0-9a-f]{32}")
    return item_id_pattern.search(dashboard_url).group(0)


def get_storymap_entries(storymap_item):
    storymap_data = storymap_item.get_data()
    return storymap_data["values"]["story"]["sections"]


def get_url_host_name(url) -> str:
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.hostname}"


def get_dashboard_version(dashboard_json):
    if dashboard_json != {} and dashboard_json is not None:
        if dashboard_json != {"_ssl": False}:  # Why is this happening?
            return dashboard_json["version"]

    return None


def get_items_from_folder(
    gis_obj, folder, item_types=None
) -> list:  # folder=None returns the root folder
    folder_items = gis_obj.users.me.items(folder=folder)

    if item_types:
        folder_items = [item for item in folder_items if item.type in item_types]

    return folder_items


def get_item_ids_from_folder(
    gis_obj, folder, item_types=None
) -> list:  # folder=None returns the root folder

    folder_items = get_items_from_folder(gis_obj, folder, item_types=item_types)
    return [item.id for item in folder_items]


def get_items_from_folders(
    gis_obj, folders: list
) -> list:  # folder=None returns the root folder
    all_items = []
    for folder in folders:
        all_items += gis_obj.users.me.items(folder=folder)

    return all_items


def get_constructed_objects_from_items(items: list) -> list:
    constructed_objects = []

    for item in items:
        if item.type == "Feature Service":
            if bool(item.url[-1].isdigit()):
                feature_layer_obj = features.FeatureLayer(url=item.url, gis=item._gis)
                feature_layer_obj = (
                    feature_layer_obj.properties
                )  # sometimes this triggers an error
                constructed_objects.append(feature_layer_obj)

            feature_layer_collection = features.FeatureLayerCollection(
                url=item.url, gis=item._gis
            )
            constructed_objects.append(feature_layer_collection)

        elif item.type == "Web Map":
            constructed_objects.append(mapping.WebMap(webmapitem=item))

        elif item.type == "Dashboard":
            try:
                constructed_objects.append(item.get_data())
            except JSONDecodeError:
                pass

    return constructed_objects


def get_constructed_layers_from_from_webmap_obj(webmap_obj, gis_obj) -> list:
    webmap_layers = webmap_obj.layers
    webmap_tables = webmap_obj.tables
    constructed_layers = []

    if webmap_layers:
        for layer in webmap_layers:
            try:
                if "url" in layer:  # Clientside layers don't have a url
                    if bool(layer.url[-1].isdigit()):
                        layer = features.FeatureLayer(url=layer.url, gis=gis_obj)
                        # sometimes accessing properties triggers an attribute error.
                        assert layer.properties
                    else:
                        layer = features.FeatureLayerCollection(
                            url=layer.url, gis=gis_obj
                        )
                        assert layer.properties

                if layer:
                    constructed_layers.append(layer)
            except Exception as e:
                if "not found" in e.args[0]:
                    continue

    if webmap_tables:
        for table in webmap_tables:
            if "url" in table:
                table = features.Table(url=table["url"], gis=gis_obj)
                if table:
                    constructed_layers.append(table)

    return constructed_layers


def get_dashboard_item_data_sources_from_dashboard_json(
    dashboard_json, gis_obj
) -> list:
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
            item = gis_obj.content.get(item_id)
        except Exception as e:
            if "Item does not exist" in e.args[0]:
                continue
            raise Exception(f"I have never seen this error: {e} before!")
        item_objs.append(item)

    return item_objs


# def get_projection_name(prj_factory_code) -> str:
#     sp_ref = osr.SpatialReference()
#     sp_ref.ImportFromEPSG(prj_factory_code)
#     return sp_ref.GetAttrValue("PROJCS")


def get_service_folder(feature_service_url, server):  # Might not work
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
        return gis.GIS(org_url, username, password, verify_cert=verify_cert)

    elif authentication_scheme.name == "iwa":
        return gis.GIS(org_url, verify_cert=verify_cert)
    elif authentication_scheme.name == "pki":
        return gis.GIS(
            org_url,
            key_file_path=key_file_path,
            cert_file_path=cert_file_path,
            verify_cert=verify_cert,
        )

    elif authentication_scheme.name == "o_auth":
        return gis.GIS(org_url, client_id=client_id, verify_cert=verify_cert)

    elif authentication_scheme.name == "server":
        return Server(
            url=org_url, username=username, password=password, verify_cert=verify_cert,
        )


# Broken
# def get_feature_from_fs_url(feature_service_url, gis_obj=None):
#
#     if is_server_url(feature_service_url) is True:
#         return FeatureLayerCollection(feature_service_url, gis=gis_obj)
#
#     else:
#         return FeatureLayer(feature_service_url, gis=gis_obj)


def get_folder_names(gis_obj) -> list:
    return gis_obj.users.me.folders


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


def get_feature_count_from_feature_layer(feature_layer) -> int:
    return feature_layer.query(return_count_only=True)


def get_files_in_directory(directory=None, extension=None) -> list:
    if directory is None:  # Loop current directory if one isn't provided
        directory = os.getcwd()

    # combine current directory with provided directory
    for path, dirs, files in os.walk(directory):
        if extension:  # Only get files with a certain extension if one is specified
            return [Path(os.path.join(path, f)) for f in files if f.endswith(extension)]
        else:
            return [Path(os.path.join(path, f)) for f in files]


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


def download_item(item, save_path=None):
    print(item.download(save_path=save_path))


if __name__ == "__main__":
    GIS_1 = MySecrets.get_agol_gis("DEV_ENV", "DBQA_REGRESSION")
    ITEM = GIS_1.content.get("7bc7b3c3625f4458b51d96da9a3dc123")
    exported_item = export_agol_item(
        ITEM, "Fire_Incidents_FGB", export_format="File Geodatabase"
    )
    print(exported_item)
