from GitHub.HelperScripts import get_funcs
import re
import requests


def check_string_for_bad_links(string):
    test_case_links = get_funcs.get_links_from_string(string)
    bad_responses = []
    for link in test_case_links:
        response = check_is_url_reachable(link)
        if not response[0]:
            bad_responses.append(response[1])

    return bad_responses


def check_string_contains_substring(string, substring) -> bool:
    pattern = re.compile(substring, re.IGNORECASE)

    if pattern.search(string):
        return True

    return False


def check_is_url_reachable(url):
    try:
        response = requests.get(url, timeout=3)
        if response.ok:
            return True, response.status_code

        else:
            return (
                False,
                f"url {url} received a response code of {response.status_code}",
            )

    except requests.exceptions.SSLError:
        return True, "There was an SSLError"

    except requests.exceptions.ConnectionError:
        return False, f"Server could not be found when attempting to access {url}"

    except requests.exceptions.ReadTimeout:
        return False, f"I timed out when attempting to access {url}"


def check_string_for_items_in_orgs(string, gis_objs: list, org_name) -> list:
    item_ids = get_funcs.get_item_ids_from_string(string)
    items = []
    try:
        for item_id in item_ids:
            item = get_funcs.get_item_from_item_id(item_id, gis_objs)
            if item:
                if check_string_contains_substring(item.homepage, org_name):
                    items.append(item.id)
    except Exception as e:
        print(e)

    return items


def check_string_for_missing_items(string, gis_objs):
    item_ids = get_funcs.get_item_ids_from_string(string)
    missing_item_ids = []
    try:
        for item_id in item_ids:
            if not get_funcs.get_item_from_item_id(item_id, gis_objs):
                missing_item_ids.append(item_id)

        return missing_item_ids

    except Exception as e:
        print(e)
