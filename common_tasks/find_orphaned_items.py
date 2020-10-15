from other.my_secrets import MySecrets
from GitHub.HelperScripts import get_funcs
import requests
from json.decoder import JSONDecodeError

gis_obj = MySecrets.get_agol_gis("DEV_ENV", "DBQA_ADMIN")
items = get_funcs.get_all_items_in_org(gis_obj, item_type="Feature Service")


with open("orphaned_items.csv", "w") as writer:
    for item in items:
        try:
            if "Invalid URL" in requests.get(item.url).text:
                writer.write(f"{item.owner}, {item.id} \n")
        except KeyError:
            pass
            # print(f"Dashboard id:{dashboard_item.id} missing 'version' in json")

        except JSONDecodeError:
            pass
            # print(f"Dashboard id:{dashboard_item.id} had an issue processing its json")

        except requests.exceptions.ConnectionError:
            pass

        except Exception as e:
            print(f"I have never seen this error before, {e}")
