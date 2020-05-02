import random
import time
import names

def add_feature_to_feature_layer(feature_layer):
    feature_set = feature_layer.query()

    feature = random.choice(feature_set.features)
    feature_set._features = [feature]
    
    feature_layer.edit_features(adds=feature_set)

def remove_feature_from_feature_layer(feature_layer):
    feature_set = feature_layer.query()

    feature_to_delete = random.choice(feature_set.features)
    feature_set._features = [feature_to_delete]
    
    feature_layer.edit_features(deletes=feature_set)

def modify_numeric_value(feature_layer):
    feature_set = feature_layer.query()

    modified_features = []
    for feature in feature_set.features:
        feature = random.choice(feature_set.features)

        feature.attributes["int_field"] = random.randint(0, 100)
        modified_features.append(feature)
    
    feature_set._features = modified_features
    
    feature_layer.edit_features(updates=feature_set)


def modify_string_value(feature_layer):
    feature_set = feature_layer.query()

    modified_features = []
    for feature in feature_set.features:
        feature = random.choice(feature_set.features)

        feature.attributes["namefield"] = names.get_full_name()
        modified_features.append(feature)
    feature_set._features = modified_features
    
    feature_layer.edit_features(updates=feature_set)


if __name__ == "__main__":
    print("I'm running all by myself")