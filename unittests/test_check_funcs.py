import unittest
from GitHub.HelperScripts import check_funcs
from other.my_secrets import MySecrets


class CheckFuncs(unittest.TestCase):
    gis_objects = MySecrets.get_admin_gis_objs()

    def test_check_string_for_bad_links(self):
        string = (
            "some text https://www.sadjklfseijo.com other text https://www.esri.com"
        )
        result = check_funcs.check_string_for_bad_links(string)
        self.assertTrue(len(result), 1)
        self.assertFalse(result[0][0])

    def test_check_string_contains_substring(self):
        string = "https://nitro.maps.devext.com"
        result = check_funcs.check_string_contains_substring(string, "nitro")
        self.assertTrue(result)

    def test_check_is_url_reachable(self):
        url = "https://www.esri.com"
        self.assertTrue(check_funcs.check_is_url_reachable(url))

    def test_check_string_for_items_in_org(self):
        string_with_item_id = "Blah blah 6d48316eb7274b0e81e30bdfe189575a Blah Blah"
        items_found = check_funcs.check_string_for_items_in_orgs(
            string_with_item_id, gis_objs=self.gis_objects
        )
        self.assertEqual(len(items_found), 1)

    def test_check_string_for_missing_items(self):
        string_with_broken_item_id = (
            "Blah blah ad483163b7274d0e81e3cbdfe189575a Blah Blah"
        )
        broken_item = check_funcs.check_string_for_missing_items(
            string_with_broken_item_id, self.gis_objects
        )

        self.assertEqual(len(broken_item), 1)
