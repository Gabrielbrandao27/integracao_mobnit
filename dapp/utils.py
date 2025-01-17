import json

def hex2str(hex):
    """
    Decodes a hex string into a regular string
    """
    return bytes.fromhex(hex[2:]).decode("utf-8")


def str2hex(str):
    """
    Encodes a string as a hex string
    """
    return "0x" + str.encode("utf-8").hex()


def dataset_to_json(keys, dataset):
    json_list = [dict(zip(keys, row)) for row in dataset]
    return json.dumps(json_list)
