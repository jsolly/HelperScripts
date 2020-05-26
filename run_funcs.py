from arcgis.apps.storymap import JournalStoryMap
from other.my_secrets import MySecrets
from GitHub.HelperScripts import get_funcs, edit_funcs

GIS_OBJ = MySecrets.get_regression_prod_dbqa_gis()

DASHBOARD_ITEMS = get_funcs.get_items_from_folder(
    GIS_OBJ, "Sharing_Options", item_types=["Dashboard"]
)
BUILD_NAME = "Develop"
BUILD_TYPE = "3x_NICKEL_BUILDER"
DASHBOARD_TYPE = "3x"
STORYMAP_ITEM = GIS_OBJ.content.get("7d84f055f6c14601bca545b9cee56628")
STORYMAP_OBJ = JournalStoryMap(gis=GIS_OBJ, item=STORYMAP_ITEM)
edit_funcs.add_dashboard_sections_to_storymap(
    storymap_obj=STORYMAP_OBJ,
    dashboard_items=DASHBOARD_ITEMS,
    build_name=BUILD_NAME,
    build_type=BUILD_TYPE,
)
STORYMAP_OBJ.save(title=f"Dashboard Embed Scenarios with {BUILD_NAME} urls")
