import unittest
import os
from other.my_secrets import get_regression_devext_dbqa_gis
from GitHub.HelperScripts import save_funcs

REGRESSION_GIS = get_regression_devext_dbqa_gis()


class MyTestCase(unittest.TestCase):
    def test_download_item_json(self):
        item = REGRESSION_GIS.content.get("d9e8b46c430e4a669e246b29fd341f13")
        save_funcs.download_item_json(item)
        self.assertTrue(os.path.isfile(f"{item.id}.json"))


if __name__ == "__main__":
    unittest.main()
