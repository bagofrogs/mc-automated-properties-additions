from json import load
from os import listdir


def loader() -> dict:
    """Generates dictionary with all the information from local json files

    Returns:
        dict: dictionary containing all the information in each json, key corresponds to filename
    """
    data_dict = {} # initialise the dict
    for file in listdir("./input-jsons"):
        if ".json" not in file or file == "template.json": # ignore non json files
            continue
        filename = file[:file.find(".json")] # cut off the .json
        data_dict[filename] = load(open("./input-jsons/" + file)) # load json from file into a python dict
    return data_dict

def merger(data_dict: dict) -> dict:
    """takes a dictionary with multiple keys that correspond to different files and merges them to obtain a single dict with blocks and items directly
    
    Args:
        data_dict (dict): a dictionary where keys are derived from filenames:
            "chipped": {
                "blocks": [
                    "description": "blabla",
                    "block_id": 12345,
                    "affected_blocks": "mod:block",
                ]
            }

    Returns:
        merged_dict: a dictionary where the different entries have been merged into one so that each block/item ID is unique
            "blocks": {
                
            }
    
    """
    merged_dict = {"block":{}, "item": {}}
    for file_key in data_dict: # filename minus .json
        for object_type in data_dict[file_key]: # block or item
            for object in data_dict[file_key][object_type]: # the actual object with description, block_id, affected_blocks
                if object["block_id"] not in merged_dict[object_type]:
                    merged_dict[object_type][object["block_id"]] = []
                merged_dict[object_type][object["block_id"]].extend(object["affected_blocks"])
    return merged_dict


def writer(merged_dict : dict):
    """Takes a merged dict and writes to local x.properties files

    Args:
        blocks_to_write (dict): a dictionary containing the blocks 
    """
    
    for object_type in merged_dict: # block or item    
        output_string = ""
        for block_id in merged_dict[object_type]:
            output_string+= "\n" + object_type + "." + str(block_id) + " = " + " ".join(merged_dict[object_type][block_id])
        file = open(mode="a", file=object_type+".properties")    
        file.write(output_string)
        file.close()

raw_dict = loader()
merged_dict = merger(raw_dict)
writer(merged_dict)