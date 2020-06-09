import unittest
from GitHub.HelperScripts import clone_funcs

from other.my_secrets import MySecrets

GIS = MySecrets.get_agol_gis("DEV_ENV", "DBQA_AUTOMATION")


class TestClass(unittest.TestCase):
    def test_clone_folder(self):
        source_folder = to_clone
        target_folder = cloned
        source_gis
        target_gis,
        copy_data = (True,)
        search_existing_items = (True,)
        ignore_item_type = (None,)
