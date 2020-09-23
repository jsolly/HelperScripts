from other.my_secrets import MySecrets
from arcgis import gis, mapping
from Devtopia.dashboard_automation.functional_tests_helper import HelperClass
from GitHub.HelperScripts import get_funcs, create_funcs, edit_funcs
from arcgis.apps.storymap import JournalStoryMap

AGOL_DICT = MySecrets.AGOL_DICT


class ArcGISOnlineTests(HelperClass):
    gis_obj = MySecrets.get_agol_gis(environment="DEV_ENV", user="DBQA_AUTOMATION")
    folder = "Sharing_Options"
    dry_run = False

    if dry_run:
        gis_obj.content.create_folder(folder="Sharing_Options")

        try:
            gis_obj.groups.create(title="Dashboard_QA_group", tags="DashboardQA")
        except Exception as e:
            if "You already have a group" in e.args[0]:
                print("This group already exists")
            else:
                raise Exception("This is an exception I have never seen before!", e)

        # Create Shared update capability group (and add members)
        gis_obj.groups.create(
            title="Shared_Update_Capability_Group",
            users_update_items=True,
            tags="DashboardQA",
        )

    def test_create_private_layer(self) -> gis.Item:
        layer_item = create_funcs.add_file_to_agol(
            gis_obj=self.gis_obj,
            file_path="../../../Data/FGBs/traffic_cameras.zip",
            agol_folder=self.folder,
            title="Private Layer",
        )
        layer_item = layer_item.publish()
        return layer_item

    def test_create_private_webmap(self) -> gis.Item:
        webmap_obj = mapping.WebMap()
        item_properties = {
            "title": "Private Webmap",
            "snippet": "This is a private webmap",
            "tags": ["DashboardQA"],
        }
        webmap_item = webmap_obj.save(
            item_properties=item_properties, folder=self.folder
        )
        return webmap_item

    def test_create_private_dashboard(self) -> gis.Item:
        self.log_into_dashboard_home()
        self.create_dashboard_from_db_home(
            title="Private Dashboard", folder=self.folder
        )
        self.add_an_element("Header")

        item_id = get_funcs.get_item_ids_from_string(self.driver.current_url)[0]
        return self.gis_obj.content.get(item_id)

    def test_create_public_layer(self) -> gis.Item:
        layer_item = create_funcs.add_file_to_agol(
            gis_obj=self.gis_obj,
            file_path="../../../Data/FGBs/Emergency_Facilities.zip",
            agol_folder=self.folder,
            title="Public Layer",
        )
        layer_item = layer_item.publish()
        layer_item.share(everyone=True)
        return layer_item

    def test_create_public_webmap(self) -> gis.Item:
        webmap_obj = mapping.WebMap()
        item_properties = {
            "title": "Public Webmap",
            "snippet": "This is a public webmap",
            "tags": ["DashboardQA"],
        }
        webmap_item = webmap_obj.save(
            item_properties=item_properties, folder=self.folder
        )
        webmap_item.share(everyone=True)
        return webmap_item

    def test_create_public_dashboard(self) -> gis.Item:
        self.log_into_dashboard_home()
        self.create_dashboard_from_db_home(title="Public Dashboard", folder=self.folder)
        self.add_an_element("Header")

        item_id = get_funcs.get_item_ids_from_string(self.driver.current_url)[0]
        item = self.gis_obj.content.get(item_id)
        item.share(everyone=True)
        return item

    def test_create_shared_to_org_layer(self) -> gis.Item:
        layer_item = create_funcs.add_file_to_agol(
            gis_obj=self.gis_obj,
            file_path="../../../Data/FGBs/Emergency_Facilities.zip",
            agol_folder=self.folder,
            title="Shared to Org Layer",
        )
        layer_item = layer_item.publish()
        layer_item.share(org=True)
        return layer_item

    def test_create_shared_to_org_webmap(self):
        webmap_obj = mapping.WebMap()
        item_properties = {
            "title": "Shared to Org Webmap",
            "snippet": "This is a Shared to Org webmap",
            "tags": ["DashboardQA"],
        }
        webmap_item = webmap_obj.save(
            item_properties=item_properties, folder=self.folder
        )
        webmap_item.share(org=True)
        return webmap_item

    def test_create_shared_to_org_dashboard(self) -> gis.Item:
        self.log_into_dashboard_home()
        self.create_dashboard_from_db_home(
            title="Shared to Org Dashboard", folder=self.folder
        )
        self.add_an_element("Header")

        dashboard_item_id = get_funcs.get_item_ids_from_string(self.driver.current_url)[
            0
        ]
        dashboard_item = self.gis_obj.content.get(dashboard_item_id)
        dashboard_item.share(org=True)
        return dashboard_item

    def test_create_shared_to_group_layer(self):
        webmap_obj = mapping.WebMap()
        item_properties = {
            "title": "Shared to Group Webmap",
            "snippet": "This is a Shared to Group webmap",
            "tags": ["DashboardQA"],
        }
        webmap_item = webmap_obj.save(
            item_properties=item_properties, folder=self.folder
        )
        group_id = get_funcs.get_group_id_from_group_name(
            self.gis_obj, "Dashboard_QA_group"
        )
        webmap_item.share(groups=[group_id])
        return webmap_item

    def test_create_shared_to_group_webmap(self):
        webmap_obj = mapping.WebMap()
        item_properties = {
            "title": "Shared to Group Webmap",
            "snippet": "This is a Shared to Group webmap",
            "tags": ["DashboardQA"],
        }
        webmap_item = webmap_obj.save(
            item_properties=item_properties, folder=self.folder
        )
        group_id = get_funcs.get_group_id_from_group_name(
            self.gis_obj, "Dashboard_QA_group"
        )
        webmap_item.share(groups=[group_id])
        return webmap_item

    def test_create_shared_to_group_dashboard(self):
        self.log_into_dashboard_home()
        self.create_dashboard_from_db_home(
            title="Shared to Group Dashboard", folder=self.folder
        )
        self.add_an_element("Header")

        item_id = get_funcs.get_item_ids_from_string(self.driver.current_url)[0]
        dashboard_item = self.gis_obj.content.get(item_id)
        group_id = get_funcs.get_group_id_from_group_name(
            self.gis_obj, "Dashboard_QA_group"
        )
        dashboard_item.share(groups=[group_id])
        return dashboard_item

    def test_create_storymap_shared_to_org_with_dashboard_urls(self):
        # # Create a storymap of Dashboards
        dashboard_items = get_funcs.get_items_from_folder(
            self.gis_obj, self.folder, item_types=["Dashboard"]
        )

        build_name = "3x Devext"
        build_type = "3X_DEV"
        # STORYMAP_ITEM = GIS.content.get("b6d09fc5da5a470fb717a5faecb283ba")
        storymap_obj = JournalStoryMap(
            gis=self.gis_obj
        )  # item=STORYMAP_ITEM if using an existing item
        edit_funcs.add_dashboard_sections_to_storymap(
            storymap_obj=storymap_obj,
            dashboard_items=dashboard_items,
            build_name=build_name,
            build_type=build_type,
            url_params="DEV_URL_PARAM",
        )
        storymap_obj.save(
            title=f"Dashboard Embed Scenarios with {build_name} urls (useParentOriginFix)"
        )
