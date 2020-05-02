def find_dashboard_ids_with_webmap(gis_user, webmap_id, orgid): # This needs work
    dashboards = gis_user.content.advanced_search(f'type: "Dashboard" AND orgid:{orgid}', max_items=2000)['results']
    dashboard_ids_dict = {}
    for dashboard_item in dashboards:
        try:
            dashboard_dict = dashboard_item.get_data()
            if "widgets" in dashboard_dict:
                for widget in dashboard_dict["widgets"]:
                    if widget["type"] == "mapWidget":
                        if widget["itemId"] == webmap_id:
                            dashboard_ids_dict[dashboard_item.owner] = dashboard_item.id
                            break # No need to find it multiple times
        except:
            pass

    return dashboard_ids_dict
