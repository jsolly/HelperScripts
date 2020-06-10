import unittest
from GitHub.HelperScripts import clone_funcs, get_funcs, edit_funcs

from other.my_secrets import MySecrets


class TestClass(unittest.TestCase):
    gis_obj = MySecrets.get_agol_gis("DEV_ENV", "DBQA_AUTOMATION")

    def test_clone_folder(self):
        self.assertEqual(len(get_funcs.get_items_from_folder(self.gis_obj, "Temp")), 0)

        clone_funcs.clone_folder(
            source_folder="To_Clone",
            target_folder="Temp",
            source_gis=self.gis_obj,
            target_gis=self.gis_obj,
        )

        self.assertGreater(
            len(get_funcs.get_items_from_folder(self.gis_obj, "Temp")), 0
        )
        edit_funcs.delete_items_from_folder(self.gis_obj, "Temp")

    def test_clone_group_to_folder(self):
        self.assertEqual(len(get_funcs.get_items_from_folder(self.gis_obj, "Temp")), 0)
        clone_funcs.clone_group_to_folder(
            source_group_id="",
            target_folder="Temp",
            source_gis_obj=self.gis_obj,
            target_gis_obj=self.gis_obj,
        )

        self.assertGreater(
            len(get_funcs.get_items_from_folder(self.gis_obj, "Temp")), 0
        )

        edit_funcs.delete_items_from_folder(self.gis_obj, "Temp")
