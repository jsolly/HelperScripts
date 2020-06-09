import unittest
from arcgis import gis, mapping, features
from GitHub.HelperScripts import get_funcs
from other.my_secrets import MySecrets

AGOL_ITEM_DICT = MySecrets.AGOL_DICT
AGOL_DICT = MySecrets.AGOL_DICT


class TestClass(unittest.TestCase):
    gis_obj = MySecrets.get_agol_gis("DEV_ENV", "DBQA_AUTOMATION")

    def test_get_group_id_from_group_name(self):
        group_id = get_funcs.get_group_id_from_group_name(
            self.gis_obj, "Dashboard_QA_group"
        )
        self.assertEqual(group_id, "9d181d2925ce48b6aac0a916497da56a")

    def test_get_links_from_string(self):
        string = "strings https://arcgis.com and more strings"
        link = get_funcs.get_links_from_string(string)
        self.assertEqual(
            link, "https://arcgis.com"
        )  # Is this testing a constant? Bad prtactice?

    def test_get_item_ids_from_string(self):
        string = """
                Sample webmap with all geom and refresh types:
                id: a540748151b84753b609d67488be363e
                org: dbqa in devext
                Sample dashboard
                id: d54f71aadaca4cd1899e133bdf3c028c
                org: dbqa in devext
                """
        item_ids = get_funcs.get_item_ids_from_string(string)
        actual_item_ids = [
            "a540748151b84753b609d67488be363e",
            "d54f71aadaca4cd1899e133bdf3c028c",
        ]

        self.assertEqual(item_ids, actual_item_ids)

    def test_get_item_from_item_id(self):
        item_id = "a540748151b84753b609d67488be363e"
        item = get_funcs.get_item_from_item_id(item_id)
        self.assertIsInstance(item, Item)

    def test_get_item_host_name(self):
        item = self.gis_obj.content.get("ec18963f29864b7baf5f5eb236f6a545")
        item_host_name = get_funcs.get_item_host_name(item)
        self.assertEqual(item_host_name, AGOL_DICT["AGOL_DBQA_DEVEXT_HOST_NAME"])

    def test_get_items_from_group(self):
        items = get_funcs.get_items_from_group(
            gis_obj=self.gis_obj, group_id="74675128c9e84b5ca3874b40df5662c6",
        )
        self.assertIsInstance(items, list)

    def test_get_file_line_count_python(self):
        file_path = "../input/covid_modified.csv"
        line_count = get_funcs.get_file_line_count_python(file_path)
        self.assertEqual(line_count, 50)

    def test_get_file_line_count_bash(self):
        file_path = "../input/covid_modified.csv"
        line_count = get_funcs.get_file_line_count_bash(file_path)
        self.assertEqual(line_count, 50)

    def test_get_func_time(self):
        def square(x, y):
            return x * y

        a, b = 2, 2
        run_time = get_funcs.get_func_run_time(square, a, b)
        self.assertIsInstance(run_time, int)

    def test_get_item_id_from_dashboard_url(self):
        url = f"{AGOL_DICT['DEV_ENV']}/apps/opsdashboard/index.html#/461ac62237774768bb40bca2b2b4c867"
        item_id = get_funcs.get_item_id_from_dashboard_url(url)
        self.assertEqual(item_id, "461ac62237774768bb40bca2b2b4c867")

    def test_get_story_map_entries(self):
        story_map_item = self.gis_obj.content.get("614a35d1a4ac4ab894efed130dee3f2a")
        entries = get_funcs.get_storymap_entries(story_map_item)
        self.assertTrue(len(entries) == 11)

    def test_get_url_host_name(self):
        url = f"{https://AGOL_DICT['DEV_ENV']}/home/content.html?view=list&sortOrder=desc&sortField=modified"
        host_name = get_funcs.get_url_host_name(url)
        self.assertEqual(host_name, AGOL_DICT["DEV_ENV"])

    def test_get_dashboard_version(self):

        dashboard_version = get_funcs.get_dashboard_version(
            AGOL_ITEM_DICT["VERSION_27_DASHBOARD_JSON"]
        )
        self.assertEqual(dashboard_version, 27)

    def test_get_items_from_folder(self):
        items = get_funcs.get_items_from_folder(self.gis_obj, "Sample_Dashboards")
        self.assertEqual(len(items), 2)

    def test_get_items_from_folders(self):
        items = get_funcs.get_items_from_folders(
            self.GIS_OBJ, ["Sample_Dashboards", "Five Items"]
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
            AGOL_ITEM_DICT["DEVEXT_WEBMAP_OBJ"], self.gis_obj
        )
        self.assertIsInstance(constructed_webmap_layers, list)
        self.assertEqual(len(constructed_webmap_layers), 3)  # Not sure if 3 is right.

    def test_get_dashboard_item_data_sources(self):
        dashboard_item_data_sources = get_funcs.get_dashboard_item_data_sources(
            AGOL_ITEM_DICT["VERSION_27_DASHBOARD_JSON"], self.gis_obj
        )
        self.assertIsInstance(dashboard_item_data_sources[0], gis.Item)
