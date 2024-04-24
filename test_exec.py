from os import listdir, path
from json import load
from json.decoder import JSONDecodeError


# test that the jsons "compile"
def json_loader(target_path) -> int:
    """Attempts to load all json files in specified directory

    Returns:
        int: exit code
    """
    for file in listdir(target_path):
        if path.isdir(target_path + "/" + file):  # folders are okay
            continue
        if ".json" not in file:
            print("ERROR: Non json file : \"" + file + "\" found in json input folder")
            return 1
        try:
            json_data = load(open(target_path + file))  # load json from file into a python dict
        except JSONDecodeError:
            print("ERROR: Json file " + file + " was incorrectly formatted and could not be loaded.")
            return 1

        # add mod ID to block IDs
        print("INFO: Checking data from " + file)
        if "id" not in json_data or "data" not in json_data:
            print("ERROR: Missing id or description fields in root data")
            return 1
        try:
            for object_type in json_data["data"]:  # go through all object types
                for object in json_data["data"][object_type]:  # go through all objects of that type
                    # check that they all have at least an id and affected objects
                    if "object_id" not in object or "affected_objects" not in object:
                        print("ERROR: Missing object_id or affected_objects in object data")
                        return 1
        except KeyError:
            print("ERROR: Json data from file: " + file + " missing essential key fields.")
    return 0


def test_json_loader():
    assert json_loader("./input-jsons/") == 0
    assert json_loader("./input-jsons/alternatives/") == 0


json_loader("./input-jsons/")
json_loader("./input-jsons/alternatives/")
