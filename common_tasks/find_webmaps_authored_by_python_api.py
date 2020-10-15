from other.my_secrets import MySecrets
from GitHub.HelperScripts import get_funcs
from arcgis.mapping import WebMap

gis_obj = MySecrets.get_agol_gis("DEV_ENV", "DBQA_ADMIN")
items = get_funcs.get_all_items_in_org(gis_obj, item_type="Web Map")

with open("python_webmaps.csv", "w") as writer:
    for item in items:
        try:
            webmap_data = item.get_data()
            if webmap_data["authoringApp"] == "ArcGISPythonAPI":
                writer.write(f"{item.owner}, {item.id}\n")

        except Exception:
            pass
