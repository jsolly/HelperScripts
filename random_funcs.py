import random
from arcgis import gis, features
from packages import edit_funcs


def randomly_move_point_feature(feature):
    try:
        new_feature_geometry = feature.get_value("geometry")
    except Exception as e:
        return feature

    new_feature_geometry["x"] += random.uniform(-100000, 10000)
    new_feature_geometry["y"] += random.uniform(-100000, 1000)

    feature.set_value("geometry", new_feature_geometry)

    webmerc_coordinate_tuple = (new_feature_geometry["x"], new_feature_geometry["y"])
    lat_long_tuple = edit_funcs.convert_projection(
        coordinate_tuple=webmerc_coordinate_tuple,
        in_prj="epsg:3857",
        out_prj="epsg:4326",
    )

    feature.set_value("lat", lat_long_tuple[0])
    feature.set_value("long", lat_long_tuple[1])

    return feature


def randomly_delete_a_point_feature_to_feature_layer(feature_layer):
    print("TODO")


def randomly_add_a_point_feature_to_feature_layer(feature_layer):
    feature_set = feature_layer.query()
    random_feature = feature_set[
        random.randint(0, len(feature_set) - 1)
    ]  # Grab a random feature from the feature set

    feature_dict = feature_set.to_dict()

    feature_layer.edit_features(updates=feature_list)


def randomly_move_point_features_in_feature_layer(feature_layer):
    feature_set = feature_layer.query()
    if feature_set.geometry_type == "esriGeometryPoint":
        feature_list = []
        for feature in feature_set:
            moved_feature = randomly_move_point_feature(feature)
            feature_list.append(moved_feature)

        feature_layer.edit_features(updates=feature_list)


if __name__ == "__main__":
    print("I'm running all by myself!")
    feature_layer = features.FeatureLayer(url="", gis=GIS_USER)
    randomly_add_a_point_feature_to_feature_layer(feature_layer)
