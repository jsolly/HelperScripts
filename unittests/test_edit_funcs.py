import unittest
from GitHub.HelperScripts import edit_funcs
from arcgis import features
from other.my_secrets import get_regression_devext_dbqa_gis

REGRESSION_GIS = get_regression_devext_dbqa_gis()


class TestClass(unittest.TestCase):
    def test_update_item_data(self):
        storymap_item = REGRESSION_GIS.content.get("d9e8b46c430e4a669e246b29fd341f13")
        item_last_modified_date = storymap_item["modified"]
        edit_funcs.update_item_data(storymap_item)
        storymap_item_new = REGRESSION_GIS.content.get(
            "d9e8b46c430e4a669e246b29fd341f13"
        )
        new_last_modified_date = storymap_item_new["modified"]
        self.assertGreater(new_last_modified_date, item_last_modified_date)

    def test_add_feature_to_feature_layer(self):
        old_feature_count = self.FEATURE_LAYER.query(return_count_only=True)
        edit_funcs.add_feature_to_feature_layer(self.FEATURE_LAYER)
        new_feature_count = self.FEATURE_LAYER.query(return_count_only=True)
        self.assertTrue(new_feature_count == old_feature_count + 1)

    def test_remove_feature_from_feature_layer(self):
        old_feature_count = self.FEATURE_LAYER.query(return_count_only=True)
        edit_funcs.remove_feature_from_feature_layer(self.FEATURE_LAYER)
        new_feature_count = self.FEATURE_LAYER.query(return_count_only=True)
        self.assertTrue(new_feature_count == old_feature_count - 1)

    def test_modify_numeric_value(self):
        old_last_edit_date = self.FEATURE_LAYER.properties.editingInfo.lastEditDate
        edit_funcs.modify_numeric_value(self.FEATURE_LAYER)
        new_feature_layer = features.FeatureLayer(self.FEATURE_LAYER.url)
        new_last_edit_date = new_feature_layer.properties.editingInfo.lastEditDate
        self.assertNotEqual(new_last_edit_date, old_last_edit_date)

    def test_modify_string_value(self):
        old_last_edit_date = self.FEATURE_LAYER.properties.editingInfo.lastEditDate
        edit_funcs.modify_string_value(self.FEATURE_LAYER)
        new_feature_layer = features.FeatureLayer(self.FEATURE_LAYER.url)
        new_last_edit_date = new_feature_layer.properties.editingInfo.lastEditDate
        self.assertNotEqual(new_last_edit_date, old_last_edit_date)
