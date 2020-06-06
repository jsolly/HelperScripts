from Devtopia.dashboard_automation.functional_tests_helper import HelperClass
from other.my_secrets import MySecrets
from GitHub.HelperScripts import get_funcs
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

AGOL_DICT = MySecrets.AGOL_DICT


class FunctionalClass(HelperClass):
    def test_copy_webmaps_to_org_folder(self):
        self.built_in_log_into_agol()
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

            arcade_folder_option = self.wait.until(
                ec.element_to_be_clickable((By.XPATH, ".//div[text()='Arcade']"))
            )

            arcade_folder_option.click()

            save_map = self.driver.find_element_by_id("save-webmap-ok_label")
            save_map.click()

    def test_overwrite_csv(self):
        # User Elisha goes to AGOL item details page
        self.driver.get(
            f"{AGOL_DICT['DEV_ENV']}/home/item.html?id=33ff12dc309d4af489d376baee4b810e"
        )
        # She sees an 'update data' button and clicks on it.
        update_data_button = self.driver.find_element_by_xpath(
            ".//button[text()='Update Data']"
        )
        update_data_button.click()
        # She wants to overwrite the whole layer, so she chooses that option
        overwrite_option = self.driver.find_element_by_xpath(
            ".//button[text()='Overwrite Entire Layer']"
        )
        # She finds the Choose file options and chooses a csv file she has on her computer
        file_input = self.driver.find_element_by_id("update-item-file")
