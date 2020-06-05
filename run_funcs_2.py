from other.my_secrets import MySecrets
from GitHub.HelperScripts import create_funcs

# PROD_GIS = MySecrets.get_agol_gis(environment="PROD_ENV", user="DBQA_REGRESSION")
# DEV_GIS = MySecrets.get_agol_gis(environment="DEV_ENV", user="DBQA_REGRESSION")
AUTOMATION_GIS = MySecrets.get_agol_gis("DEV_ENV", "DBQA_AUTOMATION")
# BUILT_IN_GIS = MySecrets.get_portal_gis(environment="BUILT-IN_ENV", user="CREATOR")
TARGET_FOLDER = "TEMP"


# Clone an item
# item = PROD_GIS.content.get("320f70a2535841a3a326e964dc78a66b")
# DEV_GIS.content.clone_items(items=[item], folder=TARGET_FOLDER)

new_item = create_funcs.add_file_to_agol(
    gis_obj=AUTOMATION_GIS,
    file_path="../../../Data/FGBs/Emergency_Facilities.zip",
    agol_folder=TARGET_FOLDER,
    title="test",
)
new_item.share(org=True)  # todo: figure out how publishing sharing works
new_item.publish()
