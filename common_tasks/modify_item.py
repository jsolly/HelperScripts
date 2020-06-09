from other.my_secrets import MySecrets

GIS = MySecrets.get_agol_gis("DEV_ENV", "DBQA_JOHN")
# Change name of item
ITEM = GIS.content.get("73933cdd8d0b4e0184b151cb9f413bbe")
item_properties = {"title": "4x Sanity Dashboard"}
ITEM.update(item_properties=item_properties)
