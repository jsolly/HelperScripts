from other.my_secrets import MySecrets
from GitHub.HelperScripts import get_funcs
from arcgis.mapping import WebMap

gis_obj = MySecrets.get_agol_gis("DEV_ENV", "DBQA_ADMIN")
items = get_funcs.get_all_items_in_org(gis_obj, item_type="Web Map")

with open("http_dashboards.csv", "w") as writer:
    for item in items:
        try:
            webmap_obj = WebMap(webmapitem=item)
        except TypeError:  # For some reason, I am getting "Web Mapping Applications"
            continue
        layers = get_funcs.get_constructed_layers_from_from_webmap_obj(
            webmap_obj, gis_obj=gis_obj
        )
        for layer in layers:
            try:
                if "https" not in layer.url:
                    writer.write(f"Item {item.id}, {layer.url}\n")
            except AttributeError:
                continue
