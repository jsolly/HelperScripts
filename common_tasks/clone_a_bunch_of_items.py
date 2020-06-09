from other.my_secrets import MySecrets
from GitHub.HelperScripts import clone_funcs

GIS = MySecrets.get_agol_gis(environment="PROD_ENV", user="DBQA_REGRESSION")
# GIS = MySecrets.get_agol_gis(environment="DEV_ENV", user="DBQA_REGRESSION")
# GIS = MySecrets.get_agol_gis("DEV_ENV", "DBQA_AUTOMATION")
# BUILT_IN_GIS = MySecrets.get_portal_gis(environment="BUILT-IN_ENV", user="CREATOR")
TARGET_FOLDER = "Arcade"


# Clone an item
# item = PROD_GIS.content.get("320f70a2535841a3a326e964dc78a66b")
# DEV_GIS.content.clone_items(items=[item], folder=TARGET_FOLDER)


# Clone a group
clone_funcs.clone_group_to_folder(
    source_group_id="dfe07fe13d154b67bbd7a38a2be90fd9",
    target_folder=TARGET_FOLDER,
    source_gis_obj=GIS,
    target_gis_obj=GIS,
    copy_data=False,
    item_types=["Web Map"],
)
