import unittest
from GitHub.HelperScripts import edit_funcs, get_funcs
from arcgis import features
from other.my_secrets import MySecrets

AGOL_DICT = MySecrets.AGOL_DICT
AGOL_ITEM_DICT = MySecrets.AGOL_ITEM_DICT
FEATURE_LAYER = AGOL_ITEM_DICT["DEVEXT_FEATURE_LAYER_ITEM"]


class TestClass(unittest.TestCase):
    gis_obj = MySecrets.get_agol_gis("DEV_ENV", "DBQA_AUTOMATION")

    # def test_swizzle_dashboard_webmaps(self):
    #     dashboard_item = self.gis_obj.content.get()
    #     webmap_dict = {
    #         "fbe59de7e1404fa694b91e231262af53": "4b22390109554cffa720c838864e4339",
    #         "fb2676810dd947eeb9d04a377376fad1": "99ab708973464b6fa4be8f673d457e7d",
    #     }  # {original, new}

    def test_delete_items_from_folder(self):
        folder = "Temp"
        self.assertGreater(
            len(get_funcs.get_items_from_folder(self.gis_obj, folder)), 0
        )

        edit_funcs.delete_items_from_folder(self.gis_obj, "Temp")

        self.assertEqual(len(get_funcs.get_items_from_folder(self.gis_obj, folder)), 0)

    def test_update_item_data(self):
        file_path = "../input/covid_modified.csv"
        item = self.gis_obj.content.get("33ff12dc309d4af489d376baee4b810e")
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
