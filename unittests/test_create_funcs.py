import unittest
from GitHub.HelperScripts import create_funcs, get_funcs

from other.my_secrets import MySecrets

SecretClass = MySecrets()

GIS = SecretClass.get_regression_devext_dbqa_gis()
# GIS = SecretClass.get_automation_devext_dbqa_gis()
# HOME = str(Path.home())


class TestClass(unittest.TestCase):
    def test_create_storymap_from_dashboards_using_specific_build(self):
        dashboard_items = get_funcs.get_items_from_folder(
            GIS, "Sharing_Options", item_types=["Dashboard"]
        )
        build_name = "release-10.8.1"
        dashboard_type = "3x"

        success = create_funcs.create_storymap_from_dashboards_using_specific_build(
            dashboard_items, build_name, dashboard_type
        )
        self.assertTrue(success)

    def test_add_file_to_agol(self):
        file_path = "../input/covid_modified.csv"
        agol_folder = "Upload"
        result_item = create_funcs.add_file_to_agol(
            gis_obj=GIS, file_path=file_path, agol_folder=agol_folder
        )
        self.assertTrue(result_item)
