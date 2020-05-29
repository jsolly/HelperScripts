from other.my_secrets import MySecrets

PROD_GIS = MySecrets.get_agol_gis(
    environment="PROD_ENV", user="DBQA_REGRESSION", password="DBQA_REGRESSION_PASSWORD"
)
DEV_GIS = MySecrets.get_agol_gis(
    environment="DEV_ENV", user="DBQA_REGRESSION", password="DBQA_REGRESSION_PASSWORD"
)
# BUILT_IN_GIS = MySecrets.get_portal_gis(environment="BUILT-IN_ENV", user="CREATOR")
TARGET_FOLDER = "_Cloned"

# Clone an item
item = PROD_GIS.content.get("320f70a2535841a3a326e964dc78a66b")
DEV_GIS.content.clone_items(items=[item], folder=TARGET_FOLDER)
