import unittest
from arcgis import gis, mapping, features
import get_funcs
from Unittests import unittest_helper

class TestClass(unittest.TestCase):
    def test_get_dashboard_version(self):
        dashboard_version = get_funcs.get_dashboard_version(self.version_27_dashboard_json)
        self.assertEqual(dashboard_version, 27)

    def test_get_items_from_folder(self):
        items = get_funcs.get_items_from_folder(self.GIS_OBJ, "Sample_Dashboards")
        self.assertEqual(len(items), 2)

    def test_get_items_from_folders(self):
        items = get_funcs.get_items_from_folders(self.GIS_OBJ, ["Sample_Dashboards", "Five Items"])
        self.assertEqual(len(items), 7)

    def test_get_constructed_objects_from_items(self):
        webmap_obj = get_funcs.get_constructed_objects_from_items([self.webmap_item], self.GIS_OBJ)[0]
        feature_layer_collection_obj = get_funcs.get_constructed_objects_from_items([self.feature_layer_collection_item],
                                                                                     self.GIS_OBJ)[0]
        dashboard_obj = get_funcs.get_constructed_objects_from_items([self.version_27_dashboard_item], self.GIS_OBJ)[0]

        self.assertIsInstance(webmap_obj, mapping.WebMap)
        self.assertIsInstance(feature_layer_collection_obj, features.FeatureLayerCollection)
        self.assertIsInstance(dashboard_obj, dict)

    def test_get_constructed_layers_from_webmap_obj(self):
        constructed_webmap_layers = get_funcs.get_constructed_layers_from_from_webmap_obj(self.webmap_obj,
                                                                                          self.GIS_OBJ)
        self.assertIsInstance(constructed_webmap_layers, list)
        self.assertEqual(len(constructed_webmap_layers), 3) # Not sure if 3 is right.

    def test_get_dashboard_item_data_sources(self):
        dashboard_item_data_sources = get_funcs.get_dashboard_item_data_sources(self.version_27_dashboard_json, self.GIS_OBJ)
        self.assertIsInstance(dashboard_item_data_sources[0], gis.Item)

    def test_get_severe_errors_from_console_log(self):
        with open("test_data/console_log.txt", 'r') as console_log:
            self.assertIn("SEVERE", get_funcs.get_severe_errors_from_console_log(console_log))


