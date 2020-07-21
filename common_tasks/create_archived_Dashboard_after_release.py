from GitHub.HelperScripts import save_funcs
from other.my_secrets import MySecrets
from Devtopia.dashboard_automation.functional_tests_helper import HelperClass

USERNAME = MySecrets.DEVTOPIA_DICT["USERNAME"]


class ArchiveDashboard(HelperClass):
    gis_obj = MySecrets.get_agol_gis("DEV_ENV", "DBQA_REGRESSION")

    def test_add_archived_dashboard(self):

        dashboard_item = self.create_dashboard_from_db_home(
            title="(3x) 8.2 Dashboard with all elements", folder="Legacy_Dashboards"
        )
        elements = {
            "Map": self.add_map,
            "Header": self.add_header,
            "Side Panel": self.add_side_panel,
            "Map Legend": self.add_map_legend,
            "Serial Chart": self.add_serial_chart,
            "Pie Chart": self.add_pie_chart,
            "Indicator": self.add_indicator,
            "Gauge": self.add_gauge,
            "List": self.add_list,
            "Details": self.add_details,
            "Rich Text": self.add_rich_text,
            "Embedded Content": self.add_an_embedded_content,
        }

        for _, func in elements.items:
            func()

        print("DONE!")
        # self.save_dashboard()
        # save_funcs.download_item_json(
        #     dashboard_item,
        #     save_location=f"/Users/{USERNAME}/Code/other/archive/reset_legacy_items/dashboard_jsons",
        # )
