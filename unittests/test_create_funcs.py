import unittest
from GitHub.HelperScripts import create_funcs, get_funcs
from other.my_secrets import MySecrets

GIS = MySecrets.get_agol_gis(environment="DEV_ENV", user="REGRESSION_DBQA")
# HOME = str(Path.home())


class TestClass(unittest.TestCase):
    def test_add_file_to_agol(self):
        file_path = "../input/covid_modified.csv"
        agol_folder = "Upload"
        result_item = create_funcs.add_file_to_agol(
            gis_obj=GIS, file_path=file_path, agol_folder=agol_folder
        )
        self.assertTrue(result_item)
