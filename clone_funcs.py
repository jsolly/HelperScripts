from pathlib import Path
import json
import traceback
from arcgis import gis, mapping, features
import get_stuff
from edit_stuff import share_all_items_in_folder
import my_secrets as secrets

def clone_folder(source_folder, target_folder, source_gis, target_gis, copy_data=True, search_existing_items=True, ignore_item_type=[]): # Make sure copy_data=true, folder, search_existing_items are set correctly

    items_list = source_gis.users.me.items(folder=source_folder)

    if ignore_item_type:
        for item in items_list:
            if item.type in ignore_item_type:
                items_list.remove(item)
    try:
        for item in items_list:
            target_gis.content.clone_items(
                        items=[item],
                        folder=target_folder,
                        copy_data=copy_data,
                        search_existing_items=search_existing_items)
    except Exception as e:
        traceback.print_exc()

def clone_group(source_group, target_group, target_folder, source_gis, target_gis, search_existing_items=True):
    source_group_items = source_gis.groups.search(query=source_group)[0].content()
    target_group = target_gis.groups.search(query=target_group)[0]

    for item in source_group_items:
        target_gis.content.clone_items(items=[item], folder=target_folder, copy_data=True, search_existing_items=True)

    target_folder_items = get_stuff.get_items_from_folder(gis_obj=target_gis, folder=target_folder)

    for item in target_folder_items:
        item.share(groups=[target_group])

def weak_clone_items(items:list, target_gis, target_folder, flip_https):
    for item in items:
        if not item.url:
            return

        if flip_https == True:
            item_url = item.url
            item_url = item_url.replace("https", "http")
        else:
            item_url = item.url
            
        item_properties = {}
        try:
            item_properties["type"] = item.type
            item_properties["title"] = item.title
            item_properties["url"] = item_url
            target_gis.content.add(item_properties=item_properties, data=item_url, folder=target_folder)
        except Exception as e:
            traceback.print_exc()

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

def save_file (data, filename, type, save_folder=None): # ~/Downloads (Work laptop)
    try:
        # if type == "geojson":
        #     data = geojson.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)

        if type == "json":
            data = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)

        with open(f"{save_folder}/{filename}.{type}","w") as outfile:
            outfile.write(data)
    except Exception as e:  
        traceback.print_exc()

def download_item_json(item, save_folder=None, pretty_json=None):

    save_folder = "../Data/JSON" if not save_folder else save_folder

    try:
        json = item.get_data()

        if pretty_json:
            json = convert_stuff.raw_json_to_pretty_json(json)

        save_file(data=json, filename=item.id, type="json", save_folder=save_folder)

    except Exception as e:
        traceback.print_exc()

def save_file_locally(data, file_name, file_ext, folder_path=None):

    folder_path = "../../Data_Output/" if folder_path is None else folder_path

    with open(f"{folder_path}{file_name}.{file_ext}") as file: 
        file.write(data)
        file.close()

def download_all_item_json_from_agol_folder(gis, agol_folder, save_folder, pretty_json=False): # "~/Downloads" mac laptop
    
    if Path(save_folder).is_dir():
        items = get_stuff.get_items_from_folder(gis=gis, folder=agol_folder)
        for item in items:
            download_item_json(item, save_folder=save_folder, pretty_json=pretty_json)
    else:
        print ("I can't find that save_folder. Can you check your spelling pretty please?")


def copy_over_map_bookmarks(webmap_item_1, webmap_item_2):
    webmap_1_obj = mapping.WebMap(webmap_item_1) 
    webmap_1_bookmarks = webmap_1_obj.definition.bookmarks
    webmap_item_2_json = webmap_item_2.get_data()
    webmap_item_2_json['bookmarks'] = webmap_1_bookmarks
    item_properties = {"text": webmap_item_2_json}
    print(webmap_item_2.update(item_properties))


def clone_ags_to_agol(gis_obj, feature_layer_url):

    #Turn Feature Layer to a Feature Set
    feature_layer = features.FeatureLayer(url=feature_layer_url)
    featureSet = feature_layer.query(where='1=1', out_fields= '*')

    #Turn FeatureSet into Feature
    feature_collection = features.FeatureCollection.from_featureset(featureSet)

    #Add the file to AGO and publish 
    fcItem = gis_obj.content.add(item_properties={
        'type': 'Feature Collection',
        'title': 'MyFeautrelayerFromFC',
        'text': feature_collection._lyr_json
    }
    )
    fcItem.publish(publish_parameters={"type":"Feature Collection", "name":"MyHostedFeautrelayerFromFC"})


if __name__ == "__main__":
    #SOURCE_FOLDER = "Embedded_Scenarios_3x"
    TARGET_FOLDER = "Vis_Details"

    ### CLONE ITEMS ####
    ITEM_IDS = [""]
    ITEMS = [gis.Item(gis=secrets.ADMIN_PROD_NITRO_GIS, itemid=ITEMID) for ITEMID in ITEM_IDS]
    secrets.REGRESSION_DEVEXT_DBQA_GIS.content.clone_items(items=ITEMS, folder=TARGET_FOLDER) #Make sure copy_data and folder params are set correctly
    #share_all_items_in_folder(TARGET_GIS, folder=TARGET_FOLDER, org=True, everyone=False)


    #### WEAK CLONE AN ITEM ####
    # ITEM = gis.Item(gis=ten_seven_saml, itemid="")
    # weak_clone_items([ITEM], target_org=GIS_USER, target_folder=TARGET_FOLDER, flip_https=True)
    # edit_stuff.share_all_items_in_folder(GIS_USER, folder=TARGET_FOLDER, org=True, everyone=False)

    #### Download an Item ####
    # ITEM = gis.Item(gis=GIS_USER, itemid="")
    # ITEM.download(save_path="~/Downloads")

    #### DOWNLOAD ITEMS with a certain type ####
    # ITEMS = get_stuff.get_items_from_folder(GIS_USER, "Sanity_Data", item_type="Dashboard")
    # for ITEM in ITEMS:
    #     ITEM.download(save_path="~/Downloads")

    
    #### WEAK CLONE A FOLDER ####
    # items = get_stuff.get_items_from_folder(GIS_USER, folder=SOURCE_FOLDER)
    # for item in items:
    #     try:
    #         weak_clone_items(items=[item], target_org=random_portal, target_folder=TARGET_FOLDER, flip_https=True)
    #     except Exception:
    #         traceback.print_exc()
            
    # edit_stuff.share_all_items_in_folder(GIS_USER, folder=TARGET_FOLDER, org=True, everyone=False)
    
    ### CLONE A SET OF ITEMS #####
    # item_ids_to_be_cloned = []
    # items_to_be_cloned = [gis.Item(gis=GIS_USER, itemid=item_id) for item_id in item_ids_to_be_cloned]
    # GIS_USER.content.clone_items(items=items_to_be_cloned, copy_data=True, folder=TARGET_FOLDER)
    # edit_stuff.share_all_items_in_folder(GIS_USER, folder=TARGET_FOLDER, org=True, everyone=False)
    
    ##### CLONE A GROUP #####
    # clone_group(source_group="V2 Dashboard Sanity Test Group", target_group="V2 Dashboard Sanity Test Group", target_folder="Data_Shared_To_Group", source_gis=GIS_USER, target_gis=L2P_DBQA_QAEXT)
 
    #### CLONE A FOLDER #####

    #PORTAL_GIS.content.create_folder(folder=SOURCE_FOLDER)
    # clone_folder(source_folder=SOURCE_FOLDER, target_folder=TARGET_FOLDER, source_gis=GIS_USER, target_gis=GIS_USER, copy_data=False)
            
    # edit_stuff.share_all_items_in_folder(L2P_NEW_SERVER, folder=TARGET_FOLDER, org=True, everyone=False)

    #### Clone Secured Items ####
    # secured_arcgis_server_feature_layer = features.FeatureLayer(gis=USER1_SECURED_SERVER, url="url")
    # secured_resource = features.FeatureLayer(gis=GIS_USER, url=""")
    
    # webmap_item_properties = {"title":"Arcgis_server_Secured_Service", "tags":"DashboardQA", "snippet":"This Webmap contains a secured service from an arcgis server"}
    # webmap = mapping.WebMap()
    # try:
    #     webmap.add_layer(secured_arcgis_server_feature_layer)
    #     webmap.save(item_properties=webmap_item_properties)
    # except Exception as e:
    #     traceback.print_exc()

    # webmap.save(item_properties=webmap_item_properties, folder=CLONE_TO_FOLDER)


    #### Download all item json from a folder ####
    #download_all_item_json_from_agol_folder(gis=GIS_USER, agol_folder="Legacy_Dashboards", save_folder="~/Documents/reset_legacy_dashboards")

    
