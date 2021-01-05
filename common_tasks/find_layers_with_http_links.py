from json.decoder import JSONDecodeError

from arcgis.mapping import WebMap

from GitHub.HelperScripts import get_funcs
from other.my_secrets import MySecrets

gis_obj = MySecrets.get_agol_gis("DEV_ENV", "DBQA_ADMIN")
webmap_items = get_funcs.get_all_items_in_org(gis_obj, item_type="Web Map")
# webmap_items = [gis_obj.content.get("3fc9f2321bf9457fac0bec3b5125b68c")]
# feature_service_items = get_funcs.get_all_items_in_org(
#     gis_obj, item_type="Feature Service"
# )


def find_http_layers_in_webmaps(webmap_items):
    for item in webmap_items:
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


def find_http_layers_in_layers(layer_items):
    for item in feature_service_items:
        if "https" not in item.url:
            writer.write(f"Item {item.id}, {item.url}, {item.type}\n")


def find_http_symbology_in_webmap(webmap_items, writer):
    for item in webmap_items:
        try:
            data = item.get_data()
            for layer_dict in data["operationalLayers"]:
                renderer_url = layer_dict["layerDefinition"]["drawingInfo"]["renderer"][
                    "symbol"
                ]["url"]
                if "https" not in renderer_url:
                    writer.write(f"Item {item.id}\n")
        except KeyError:
            pass

        except JSONDecodeError:
            pass


if __name__ == "__main__":
    with open("http_symbology.csv", "w") as writer:
        find_http_symbology_in_webmap(webmap_items, writer)
