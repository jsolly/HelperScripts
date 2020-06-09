from Devtopia.dashboard_automation.functional_tests_helper import HelperClass
from other.my_secrets import MySecrets
from GitHub.HelperScripts import get_funcs
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import time

AGOL_DICT = MySecrets.AGOL_DICT


class FunctionalClass(HelperClass):
    def test_create_dashboards_from_inside_webmaps_and_place_in_folder(self):
        target_folder = "Arcade_try_again"
        webmap_folder_items = get_funcs.get_items_from_folder(
            self.gis_obj, folder="Arcade_try_again", item_types=["Web Map"]
        )

        self.log_into_org()
        self.driver.get(f"{self.gis_obj.url}/home/webmap/viewer.html?useExisting=1")

        mvb_banner_close = self.wait.until(
            ec.element_to_be_clickable((By.XPATH, f".//span[text()='Not right now']"))
        )
        mvb_banner_close.click()

        for webmap_item in webmap_folder_items:
            self.driver.get(
                f"{self.gis_obj.url}/home/webmap/viewer.html?webmap={webmap_item.id}"
            )
            time.sleep(3)  # Webmap chokes if you move too quickly

            share_button = self.wait.until(
                ec.element_to_be_clickable(
                    (By.XPATH, ".//span[@widgetid='webmap-share']")
                )
            )
            share_button.click()

            create_web_app_button = self.wait.until(
                ec.element_to_be_clickable(
                    (By.ID, "button-share-map-application_label")
                )
            )
            create_web_app_button.click()

            time.sleep(3)

            arcgis_dashboards_tab = self.wait.until(
                ec.element_to_be_clickable((By.ID, "opDashboardTab"))
            )
            arcgis_dashboards_tab.click()
            time.sleep(3)

            folder_dropdown = self.wait.until(
                ec.element_to_be_clickable(
                    (
                        By.ID,
                        "arcgisonline_sharing_dijit_dialog_ItemPropertiesDlg_0-folders",
                    )
                )
            )
            folder_dropdown.click()

            time.sleep(3)

            folder_option = self.wait.until(
                ec.element_to_be_clickable(
                    (By.XPATH, f".//td[text()='{target_folder}']")
                )
            )

            folder_option.click()

            time.sleep(3)

            done_button = self.wait.until(
                ec.element_to_be_clickable((By.ID, "publish-webmap-button_label"))
            )
            done_button.click()
            time.sleep(3)

    def copy_webmaps_to_org_folder(self):
        self.log_into_org()
        self.go_to_agol_content_page()
        target_folder = "Arcade"
        group_webmap_items = get_funcs.get_items_from_group(
            gis_obj=self.gis_obj,
            group_id="dfe07fe13d154b67bbd7a38a2be90fd9",
            item_types=["Web Map"],
        )

        webmap_ids = [webmap_item.id for webmap_item in group_webmap_items]

        for webmap_id in webmap_ids:
            self.driver.get(
                f"{self.gis_obj.url}/home/webmap/viewer.html?webmap={webmap_id}"
            )
            save_button = self.wait.until(
                ec.element_to_be_clickable(
                    (By.XPATH, ".//span[@widgetid='webmap-save']")
                )
            )
            save_button.click()

            save_as_option = self.driver.find_element_by_xpath(
                ".//tr[@widgetid='webmap-save-saveas']"
            )
            save_as_option.click()

            save_in_folder_dropdown = self.wait.until(
                ec.element_to_be_clickable(
                    (By.XPATH, ".//input[contains(@class, 'dijitArrowButtonInner')]")
                )
            )
            save_in_folder_dropdown.click()

            folder_option = self.wait.until(
                ec.element_to_be_clickable(
                    (By.XPATH, f".//div[text()='{target_folder}']")
                )
            )

            folder_option.click()

            save_map = self.driver.find_element_by_id("save-webmap-ok_label")
            save_map.click()
