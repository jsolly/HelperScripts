from GitHub.HelperScripts import clone_funcs
from other.my_secrets import MySecrets

# GIS = MySecrets.get_agol_gis(environment="PROD_ENV", user="DBQA_ADMIN")
GIS_2 = MySecrets.get_agol_gis(environment="DEV_ENV", user="DBQA_REGRESSION")
# GIS_3 = MySecrets.get_agol_gis(environment="DEV_ENV", user="DBQA_ADMIN")
GIS_4 = MySecrets.get_agol_gis(environment="DEV_ENV", user="NITRO_ADMIN")
# IS_5 = MySecrets.get_agol_gis(environment="DEV_ENV", user="DBQA_JOHN")
# GIS_6 = MySecrets.get_agol_gis(environment="DEV_ENV", user="DBQA_PUBLISHER")
# GIS_7 = gis.GIS("https://devext.arcgis.com", "mtest_11_10_2020_11_56_36", "Testtest11")
# GIS = MySecrets.get_agol_gis("DEV_ENV", "DBQA_AUTOMATION")
# BUILT_IN_GIS = MySecrets.get_portal_gis(environment="BUILT-IN_ENV", user="CREATOR")
# MY_PORTAL = MySecrets.get_portal_gis(environment="MY_PORTAL", user="ENT_REGRESSION")
TARGET_FOLDER = "_Cloned"


# Clone an item
# item = GIS.content.get("2fc9ef59aacf4d67b8391c845baf0edc")
# GIS_2.content.clone_items(items=[item], folder=TARGET_FOLDER)


# Clone a group
# clone_funcs.clone_group_to_folder(
#     source_group_id="bd43716d950c4aba9b6728750f97b6ca",
#     target_folder=TARGET_FOLDER,
#     source_gis_obj=GIS,
#     target_gis_obj=GIS,
#     copy_data=False,
#     item_types=["Web Map"],
# )

# Clone a folder
clone_funcs.clone_folder(
    "Sharing_Options_Dashboards_Edge_Cases",
    "Sharing_Options_Dashboards_Edge_Cases",
    GIS_2,
    GIS_4,
)
