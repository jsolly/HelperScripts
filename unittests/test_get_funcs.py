import unittest
from arcgis import gis, mapping, features
from GitHub.HelperScripts import get_funcs
from other.my_secrets import AGOL_ITEM_DICT, get_automation_devext_dbqa_gis

AUTOMATION_DEVEXT_DBQA_GIS = get_automation_devext_dbqa_gis()


class TestClass(unittest.TestCase):
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
        items = get_funcs.get_items_from_folder(
            AUTOMATION_DEVEXT_DBQA_GIS, "Sample_Dashboards"
        )
        self.assertEqual(len(items), 2)

    def test_get_items_from_folders(self):
        items = get_funcs.get_items_from_folders(
            AUTOMATION_DEVEXT_DBQA_GIS, ["Sample_Dashboards", "Five Items"]
        )
        self.assertEqual(len(items), 7)

    def test_get_constructed_objects_from_items(self):
        webmap_obj = get_funcs.get_constructed_objects_from_items(
            [AGOL_ITEM_DICT["DEVEXT_WEBMAP_OBJ"]], AUTOMATION_DEVEXT_DBQA_GIS
        )[0]
        feature_layer_collection_obj = get_funcs.get_constructed_objects_from_items(
            [AGOL_ITEM_DICT["DEVEXT_FEATURE_LAYER_COLLECTION_ITEM"]],
            AUTOMATION_DEVEXT_DBQA_GIS,
        )[0]
        dashboard_obj = get_funcs.get_constructed_objects_from_items(
            [AGOL_ITEM_DICT["DEVEXT_VERSION_27_DASHBOARD_ITEM"]],
            AUTOMATION_DEVEXT_DBQA_GIS,
        )[0]

        self.assertIsInstance(webmap_obj, mapping.WebMap)
        self.assertIsInstance(
            feature_layer_collection_obj, features.FeatureLayerCollection
        )
        self.assertIsInstance(dashboard_obj, dict)

    def test_get_constructed_layers_from_webmap_obj(self):
        constructed_webmap_layers = get_funcs.get_constructed_layers_from_from_webmap_obj(
            AGOL_ITEM_DICT["DEVEXT_WEBMAP_OBJ"], AUTOMATION_DEVEXT_DBQA_GIS
        )
        self.assertIsInstance(constructed_webmap_layers, list)
        self.assertEqual(len(constructed_webmap_layers), 3)  # Not sure if 3 is right.

    def test_get_dashboard_item_data_sources(self):
        dashboard_item_data_sources = get_funcs.get_dashboard_item_data_sources(
            AGOL_ITEM_DICT["VERSION_27_DASHBOARD_JSON"], AUTOMATION_DEVEXT_DBQA_GIS
        )
        self.assertIsInstance(dashboard_item_data_sources[0], gis.Item)
