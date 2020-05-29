from arcgis.apps.storymap import JournalStoryMap
from other.my_secrets import MySecrets
from GitHub.HelperScripts import get_funcs, edit_funcs

# PROD_GIS = MySecrets.get_regression_prod_dbqa_gis()
# DEV_GIS = MySecrets.get_regression_devext_dbqa_gis()
BUILT_IN_GIS = MySecrets.get_portal_gis(environment="BUILT-IN_ENV", user="CREATOR")
TARGET_FOLDER = "_Cloned"

# # Clone an item
# item = PROD_GIS.content.get("550136ea2c17474da709fcb5367a167b")
# DEV_GIS.content.clone_items(items=[item], folder=TARGET_FOLDER)


# # Create a storymap of Dashboards
BUILT_IN_GIS.content.create_folder("Sharing_Options")
DASHBOARD_ITEMS = get_funcs.get_items_from_folder(
    BUILT_IN_GIS, "Sharing_Options", item_types=["Dashboard"]
)

BUILD_NAME = "10.8.1 Built-in Enterprise Portal"
BUILD_TYPE = "MY_PORTAL"
# STORYMAP_ITEM = BUILT_IN_GIS.content.get("b6d09fc5da5a470fb717a5faecb283ba")
STORYMAP_OBJ = JournalStoryMap(
    gis=BUILT_IN_GIS
)  # item=STORYMAP_ITEM if using an existing item
edit_funcs.add_dashboard_sections_to_storymap(
    storymap_obj=STORYMAP_OBJ,
    dashboard_items=DASHBOARD_ITEMS,
    build_name=BUILD_NAME,
    build_type=BUILD_TYPE,
)
STORYMAP_OBJ.save(title=f"Dashboard Embed Scenarios with {BUILD_NAME} urls")
