from other.my_secrets import MySecrets
from GitHub.HelperScripts import get_funcs

GIS = MySecrets.get_agol_gis("PROD_ENV", "DBQA_REGRESSION")
# Change name of items
ITEMS = get_funcs.get_items_from_folder(
    gis_obj=GIS, folder="Arcade_Dashboards", item_types=["Dashboard"]
)

for ITEM in ITEMS:
    if "(copy)" in ITEM.title:
        item_properties = {"title": ITEM.title.replace("(copy)", "- 4x")}
        ITEM.update(item_properties=item_properties)
