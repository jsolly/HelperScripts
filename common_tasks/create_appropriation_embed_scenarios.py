from arcgis.apps.storymap import JournalStoryMap

from GitHub.HelperScripts import get_funcs
from other.my_secrets import MySecrets

AGOL_DICT = MySecrets.AGOL_DICT
NICKEL_BUILDER = AGOL_DICT["NICKEL_BUILDER_HOST_NAME"]
PORTAL_DICT = MySecrets.PORTAL_DICT


def add_dashboard_sections_to_storymap(
    storymap_obj, dashboard_items: list, build_name, build_type, title, url_params=None,
):
    dashboard_url_dict = {
        "3X_NICKEL_BUILDER": f"{NICKEL_BUILDER}/{build_name}/#",
        "4X_NICKEL_BUILDER": f"{NICKEL_BUILDER}/{build_name}/dashboards",
        "4X_DEV_GENERIC": f"{AGOL_DICT['DEV_ENV']}/apps/dashboards",
        "3X_DEV_GENERIC": f"{AGOL_DICT['DEV_ENV']}/apps/opsdashboard/index.html#",
        "4X_DEV_ORG": f"{AGOL_DICT['DEV_ORG_ENV']}/apps/dashboards",
        "3X_DEV_ORG": f"{AGOL_DICT['DEV_ORG_ENV']}/apps/opsdashboard/index.html#",
        "4X_PROD_GENERIC": f"{AGOL_DICT['PROD_ENV']}/apps/dashboards",
        "3X_PROD_GENERIC": f"{AGOL_DICT['PROD_ENV']}/apps/opsdashboard/index.html#",
        "4X_PROD_ORG": f"{AGOL_DICT['PROD_ORG_ENV']}/apps/dashboards",
        "3X_PROD_ORG": f"{AGOL_DICT['PROD_ORG_ENV']}/apps/opsdashboard/index.html#",
        "MY_PORTAL": f"{PORTAL_DICT['MY_PORTAL']}/apps/opsdashboard/index.html#",
    }
    storymap_obj.add(
        title=title, content="Example Website", url_or_item="https://www.example.com",
    )
    url_params = "" if not url_params else AGOL_DICT[url_params]

    for dashboard_item in dashboard_items:
        parameter_seperator = "?" if "3X" in build_type else "#"
        dashboard_url = f"https://{dashboard_url_dict[build_type]}/{dashboard_item.id}{parameter_seperator}{url_params}"

        storymap_obj.add(
            title=f"{dashboard_item.title} {build_name}",
            content=f"{dashboard_item.title} {build_name}",
            url_or_item=dashboard_url,
        )

    return storymap_obj


if __name__ == "__main__":
    # GIS_OBJ = MySecrets.get_agol_gis("DEV_ENV", "DBQA_REGRESSION")

    DBQA_GIS_OBJ = MySecrets.get_portal_gis(
        environment="MY_PORTAL", user="ENT_REGRESSION"
    )
    NITRO_GIS_OBJ = MySecrets.get_portal_gis(
        environment="3X_DEV_ORG", user="NITRO_ADMIN"
    )
    dashboard_items = get_funcs.get_items_from_folder(
        DBQA_GIS_OBJ, "Sharing_Options_Dashboards_Edge_Cases", item_types=["Dashboard"]
    )
    build_name = "10.8.1 Enterprise Portal Classic Dashboards"
    build_type = "MY_PORTAL"
    title = f"Dashboard in-depth Embed Scenarios with {build_name} urls {build_type}"
    # url_params = AGOL_DICT["DEV_URL_PARAM"]
    storymap = JournalStoryMap(DBQA_GIS_OBJ)
    storymap_obj = add_dashboard_sections_to_storymap(
        storymap_obj=storymap,
        dashboard_items=dashboard_items,
        build_name=build_name,
        build_type=build_type,
        title=title,
        url_params=None,
    )
    storymap_obj.save(title=title)
