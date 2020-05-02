import unittest
from dashboard_automation import modify_funcs
from Unittests import unittest_helper
from arcgis import features

class TestClass(unittest.TestCase):

    def test_add_feature_to_feature_layer(self):
        old_feature_count = self.FEATURE_LAYER.query(return_count_only=True)
        modify_funcs.add_feature_to_feature_layer(self.FEATURE_LAYER)
        new_feature_count = self.FEATURE_LAYER.query(return_count_only=True)
        self.assertTrue(new_feature_count == old_feature_count + 1)

    def test_remove_feature_from_feature_layer(self):
        old_feature_count = self.FEATURE_LAYER.query(return_count_only=True)
        modify_funcs.remove_feature_from_feature_layer(self.FEATURE_LAYER)
        new_feature_count = self.FEATURE_LAYER.query(return_count_only=True)
        self.assertTrue(new_feature_count == old_feature_count - 1)

    def test_modify_numeric_value(self):
        old_last_edit_date = self.FEATURE_LAYER.properties.editingInfo.lastEditDate
        modify_funcs.modify_numeric_value(self.FEATURE_LAYER)
        new_feature_layer = features.FeatureLayer(self.FEATURE_LAYER.url)
        new_last_edit_date = new_feature_layer.properties.editingInfo.lastEditDate
        self.assertNotEqual(new_last_edit_date, old_last_edit_date)

    def test_modify_string_value(self):
        old_last_edit_date = self.FEATURE_LAYER.properties.editingInfo.lastEditDate
        modify_funcs.modify_string_value(self.FEATURE_LAYER)
        new_feature_layer = features.FeatureLayer(self.FEATURE_LAYER.url)
        new_last_edit_date = new_feature_layer.properties.editingInfo.lastEditDate
        self.assertNotEqual(new_last_edit_date, old_last_edit_date)