import unittest
from GitHub.HelperScripts import edit_funcs
from arcgis import features
from other.my_secrets import MySecrets

GIS_OBJ = MySecrets.get_automation_devext_dbqa_gis()
AGOL_DICT = MySecrets
AGOL_ITEM_DICT = MySecrets.AGOL_ITEM_DICT
FEATURE_LAYER = AGOL_ITEM_DICT["DEVEXT_FEATURE_LAYER_ITEM"]


class TestClass(unittest.TestCase):
    def test_update_item_data(self):
        file_path = "../input/covid_modified.csv"
        item = GIS_OBJ.content.get("33ff12dc309d4af489d376baee4b810e")
        update = edit_funcs.update_item_data(item, file_path)
        self.assertTrue(update)

    def test_add_feature_to_feature_layer(self):
        old_feature_count = FEATURE_LAYER.query(return_count_only=True)
        edit_funcs.add_feature_to_feature_layer(FEATURE_LAYER)
        new_feature_count = FEATURE_LAYER.query(return_count_only=True)
        self.assertTrue(new_feature_count == old_feature_count + 1)

    def test_remove_feature_from_feature_layer(self):
        old_feature_count = FEATURE_LAYER.query(return_count_only=True)
        edit_funcs.remove_feature_from_feature_layer(FEATURE_LAYER)
        new_feature_count = FEATURE_LAYER.query(return_count_only=True)
        self.assertTrue(new_feature_count == old_feature_count - 1)

    def test_modify_numeric_value(self):
        old_last_edit_date = FEATURE_LAYER.properties.editingInfo.lastEditDate
        edit_funcs.modify_numeric_value(FEATURE_LAYER)
        new_feature_layer = features.FeatureLayer(FEATURE_LAYER.url)
        new_last_edit_date = new_feature_layer.properties.editingInfo.lastEditDate
        self.assertNotEqual(new_last_edit_date, old_last_edit_date)

    def test_modify_string_value(self):
        old_last_edit_date = FEATURE_LAYER.properties.editingInfo.lastEditDate
        edit_funcs.modify_string_value(FEATURE_LAYER)
        new_feature_layer = features.FeatureLayer(FEATURE_LAYER.url)
        new_last_edit_date = new_feature_layer.properties.editingInfo.lastEditDate
        self.assertNotEqual(new_last_edit_date, old_last_edit_date)
