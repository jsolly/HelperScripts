from other.my_secrets import MySecrets
from GitHub.HelperScripts import get_funcs
from arcgis.apps.storymap import JournalStoryMap

AGOL_DICT = MySecrets.AGOL_DICT
NICKEL_BUILDER = AGOL_DICT["NICKEL_BUILDER_HOST_NAME"]
PORTAL_DICT = MySecrets.PORTAL_DICT


def add_webmap_sections_to_storymap(storymap_obj, webmap_items):

    for webmap_item in webmap_items:

        storymap_obj.add(
            title=webmap_item.title, content=webmap_item.title, url_or_item=webmap_item,
        )

    return storymap_obj


if __name__ == "__main__":
    gis_obj = MySecrets.get_agol_gis("DEV_ENV", "DBQA_REGRESSION")
    webmap_items = get_funcs.get_items_from_folder(
        gis_obj, "Sharing_Options", item_types=["Web Map"]
    )
    storymap = JournalStoryMap(gis_obj)
    storymap_obj = add_webmap_sections_to_storymap(
        storymap_obj=storymap, webmap_items=webmap_items,
    )
    storymap_obj.save(
        title=f"Public Storymap with Embed Scenarios featuring different web maps"
    )
