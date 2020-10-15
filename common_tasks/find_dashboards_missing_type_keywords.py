from other.my_secrets import MySecrets
from GitHub.HelperScripts import get_funcs
from json.decoder import JSONDecodeError

gis_obj = MySecrets.get_agol_gis("DEV_ENV", "DBQA_ADMIN")
dashboard_items = get_funcs.get_all_items_in_org(gis_obj)

with open("missing_typekeywords.csv", "w") as writer:
    for dashboard_item in dashboard_items:
        try:
            dashboard_json = dashboard_item.get_data()
            if dashboard_json["version"] > 40:
                if "ArcGIS Dashboards" not in dashboard_item.typeKeywords:
                    writer.write(f"{dashboard_item.owner}, {dashboard_item.id}\n")
        except KeyError:
            pass
            # print(f"Dashboard id:{dashboard_item.id} missing 'version' in json")

        except JSONDecodeError:
            pass
            # print(f"Dashboard id:{dashboard_item.id} had an issue processing its json")
