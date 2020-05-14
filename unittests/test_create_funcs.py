import unittest
from other.my_secrets import get_regression_devext_dbqa_gis
from GitHub.HelperScripts import create_funcs
from GitHub.HelperScripts.get_funcs import get_items_from_folder

REGRESSION_DBQA_GIS = get_regression_devext_dbqa_gis()


class MyTestCase(unittest.TestCase):
    def test_add_and_publish_file(self):
        create_funcs.add_and_publish_file(
            REGRESSION_DBQA_GIS,
            "614a35d1a4ac4ab894efed130dee3f2a.json",
            file_type="Web Mapping Application",
            agol_folder="_Cloned",
            title="Story Map with various dashboards with different sharing settings (3x PR Dashboard URLS)",
        )

    def test_create_storymap_from_dashboards_using_pr(self):
        dashboards_to_add = get_items_from_folder(
            REGRESSION_DBQA_GIS, "Sharing_Options", item_types=["Dashboard"]
        )
        create_funcs.create_storymap_from_dashboards_using_pr(
            dashboards_to_add, 4464, "3x"
        )


if __name__ == "__main__":
    unittest.main()
