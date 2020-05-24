import unittest
from arcgis import gis, mapping, features
from GitHub.HelperScripts import get_funcs
from other.my_secrets import MySecrets

AGOL_ITEM_DICT = MySecrets.AGOL_DICT
GIS_OBJ = MySecrets.get_automation_devext_dbqa_gis()


class TestClass(unittest.TestCase):
    def test_get_func_time(self):
        def square(a, b):
            return a * b

        a, b = 2, 2
        run_time = get_funcs.get_func_run_time(square, a, b)
        self.assertIsInstance(run_time, int)

    def test_get_item_id_from_dashboard_url(self):
        url = "https://devext.arcgis.com/apps/opsdashboard/index.html#/461ac62237774768bb40bca2b2b4c867"  # todo: remove url
        item_id = get_funcs.get_item_id_from_dashboard_url(url)
        self.assertEqual(item_id, "461ac62237774768bb40bca2b2b4c867")

    def test_get_story_map_entries(self):
        story_map_item = GIS_OBJ.content.get("614a35d1a4ac4ab894efed130dee3f2a")
        entries = get_funcs.get_storymap_entries(story_map_item)
        self.assertTrue(len(entries) == 11)

    def test_get_url_host_name(self):
        url = "https://dbqa.mapsdevext.arcgis.com/home/content.html?view=list&sortOrder=desc&sortField=modified"
        host_name = get_funcs.get_url_host_name(url)
        self.assertEqual(host_name, "dbqa.mapsdevext.arcgis.com")

    def test_get_dashboard_version(self):

        dashboard_version = get_funcs.get_dashboard_version(
            AGOL_ITEM_DICT["VERSION_27_DASHBOARD_JSON"]
        )
        self.assertEqual(dashboard_version, 27)

    def test_get_items_from_folder(self):
        items = get_funcs.get_items_from_folder(GIS_OBJ, "Sample_Dashboards")
        self.assertEqual(len(items), 2)

    def test_get_items_from_folders(self):
        items = get_funcs.get_items_from_folders(
            GIS_OBJ, ["Sample_Dashboards", "Five Items"]
        )
        self.assertEqual(len(items), 7)

    def test_get_constructed_objects_from_items(self):
        webmap_obj = get_funcs.get_constructed_objects_from_items(
            [AGOL_ITEM_DICT["DEVEXT_WEBMAP_OBJ"]], GIS_OBJ
        )[0]
        feature_layer_collection_obj = get_funcs.get_constructed_objects_from_items(
            [AGOL_ITEM_DICT["DEVEXT_FEATURE_LAYER_COLLECTION_ITEM"]], GIS_OBJ,
        )[0]
        dashboard_obj = get_funcs.get_constructed_objects_from_items(
            [AGOL_ITEM_DICT["DEVEXT_VERSION_27_DASHBOARD_ITEM"]], GIS_OBJ,
        )[0]

        self.assertIsInstance(webmap_obj, mapping.WebMap)
        self.assertIsInstance(
            feature_layer_collection_obj, features.FeatureLayerCollection
        )
        self.assertIsInstance(dashboard_obj, dict)

    def test_get_constructed_layers_from_webmap_obj(self):
        constructed_webmap_layers = get_funcs.get_constructed_layers_from_from_webmap_obj(
            AGOL_ITEM_DICT["DEVEXT_WEBMAP_OBJ"], GIS_OBJ
        )
        self.assertIsInstance(constructed_webmap_layers, list)
        self.assertEqual(len(constructed_webmap_layers), 3)  # Not sure if 3 is right.

    def test_get_dashboard_item_data_sources(self):
        dashboard_item_data_sources = get_funcs.get_dashboard_item_data_sources(
            AGOL_ITEM_DICT["VERSION_27_DASHBOARD_JSON"], GIS_OBJ
        )
        self.assertIsInstance(dashboard_item_data_sources[0], gis.Item)

    def test_get_lines_in_file(self):
        file_path = "../input/Date_with_string_date_time_2_0.csv"
        line_count = get_funcs.count_lines_in_file(file_path)
        self.assertEqual(line_count, 1000)
