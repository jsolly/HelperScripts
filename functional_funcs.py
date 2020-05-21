from Devtopia.dashboard_automation.Functional_Tests import (
    functional_tests_helper as helper,
)
from other.my_secrets import MySecrets

AGOL_DICT = MySecrets.AGOL_DICT


class FunctionalClass(helper.HelperClass):
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
