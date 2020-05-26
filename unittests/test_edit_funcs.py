import unittest
from GitHub.HelperScripts import edit_funcs, get_funcs
from arcgis import features
from other.my_secrets import MySecrets
from arcgis.apps.storymap import JournalStoryMap

GIS_OBJ = MySecrets.get_automation_devext_dbqa_gis()
AGOL_DICT = MySecrets.AGOL_DICT
AGOL_ITEM_DICT = MySecrets.AGOL_ITEM_DICT
FEATURE_LAYER = AGOL_ITEM_DICT["DEVEXT_FEATURE_LAYER_ITEM"]


class TestClass(unittest.TestCase):
    def test_add_dashboard_sections_to_storymap(self):
        dashboard_items = get_funcs.get_items_from_folder(
            GIS_OBJ, "7_Dashboards", item_types=["Dashboard"]
        )
        build_name = "release-10.8.1"
        build_type = "3x_NICKEL_BUILDER"
        url_params = AGOL_DICT["DEV_URL_PARAM"]
        storymap = JournalStoryMap(gis=GIS_OBJ)
        storymap_obj = edit_funcs.add_dashboard_sections_to_storymap(
            storymap_obj=storymap,
            dashboard_items=dashboard_items,
            build_name=build_name,
            build_type=build_type,
            url_params=url_params,
        )
        storymap_sections = storymap_obj.properties["values"]["story"]["sections"]
        self.assertEqual(len(storymap_sections), 8)
        storymap_obj.save(title=f"Dashboard Embed Scenarios with {build_name} urls")

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
