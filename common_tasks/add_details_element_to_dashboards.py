from Devtopia.dashboard_automation.functional_tests_helper import HelperClass
from other.my_secrets import MySecrets
from GitHub.HelperScripts import get_funcs
import time

AGOL_DICT = MySecrets.AGOL_DICT


class ExampleClass(HelperClass):
    def test_add_details_element_to_dashboards_all_layers(self):
        dashboard_item_ids = get_funcs.get_item_ids_from_folder(
            self.gis_obj, folder="Arcade_Dashboards", item_types=["Dashboard"]
        )

        self.log_into_org()
        for dashboard_id in dashboard_item_ids[19:]:
            self.open_dashboard(dashboard_id=dashboard_id, parameters="#mode=edit")
            time.sleep(5)  # wait for layers to load
            self.add_an_element("Details", all_layers=True)
            self.save_dashboard()
