from arcgis.apps.storymap import JournalStoryMap
from other.my_secrets import MySecrets
from GitHub.HelperScripts import get_funcs, edit_funcs

# PROD_GIS = MySecrets.get_agol_gis(
#     "PROD_ENV", "DBQA_REGRESSION", "DBQA_REGRESSION_PASSWORD"
# )
# GIS = MySecrets.get_regression_devext_dbqa_gis()
GIS = MySecrets.get_agol_gis("DEV_ENV", "DBQA_REGRESSION")
TARGET_FOLDER = "Sharing_Options"

# # Create a storymap of Dashboards
DASHBOARD_ITEMS = get_funcs.get_items_from_folder(
    GIS, "Sharing_Options", item_types=["Dashboard"]
)

BUILD_NAME = "release-10.8.1"
BUILD_TYPE = "3x_NICKEL_BUILDER"
# STORYMAP_ITEM = GIS.content.get("b6d09fc5da5a470fb717a5faecb283ba")
STORYMAP_OBJ = JournalStoryMap(gis=GIS)  # item=STORYMAP_ITEM if using an existing item
edit_funcs.add_dashboard_sections_to_storymap(
    storymap_obj=STORYMAP_OBJ,
    dashboard_items=DASHBOARD_ITEMS,
    build_name=BUILD_NAME,
    build_type=BUILD_TYPE,
    url_params="DEV_URL_PARAM",
)
STORYMAP_OBJ.save(title=f"Dashboard Embed Scenarios with {BUILD_NAME} urls")
