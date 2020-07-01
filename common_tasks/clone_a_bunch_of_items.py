from other.my_secrets import MySecrets
from GitHub.HelperScripts import clone_funcs

GIS = MySecrets.get_agol_gis(environment="PROD_ENV", user="DBQA_ADMIN")
GIS_2 = MySecrets.get_agol_gis(environment="DEV_ENV", user="DBQA_REGRESSION")
# GIS_3 = MySecrets.get_agol_gis(environment="DEV_ENV", user="DBQA_ADMIN")
# GIS = MySecrets.get_agol_gis("DEV_ENV", "DBQA_AUTOMATION")
# BUILT_IN_GIS = MySecrets.get_portal_gis(environment="BUILT-IN_ENV", user="CREATOR")
TARGET_FOLDER = "Mobile_Phone_Tablet"


# Clone an item
item = GIS.content.get("d5e7d2c4e15e4344a61baeaf6466835c")
GIS_2.content.clone_items(items=[item], folder=TARGET_FOLDER)

# 'fb2676810dd947eeb9d04a377376fad1'
# 'fbe59de7e1404fa694b91e231262af53'


# Clone a group
# clone_funcs.clone_group_to_folder(
#     source_group_id="bd43716d950c4aba9b6728750f97b6ca",
#     target_folder=TARGET_FOLDER,
#     source_gis_obj=GIS,
#     target_gis_obj=GIS,
#     copy_data=False,
#     item_types=["Web Map"],
# )
