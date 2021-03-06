from redis import Redis
import json

# Redis server
r_server = Redis(host='localhost',port='6379', db='0')


def create_item(item_dict):

    """
    Set/Update item in Redis

    Args: 
        item_dict(dictionary): item 
        to be put/updated in Redis
    """
    
    try:
        deserialized_item = json.loads(item_dict)
        item_key = deserialized_item["key"]
        r_server.set(item_key, item_dict)
        result = {"status": 1, "message": "Item Created", "item": deserialized_item}

    except (Exception) as e:
        error = type(e)
        result = {"status": 0, "message": "Error", "error": error}

    return result


def delete_item(item_dict):

    """ 
    Delete item in Redis

    Args: 
        item_dict(dictionary): item 
        to be deleted in Redis
    """

    try:
        deserialized_item = json.loads(item_dict)
        item_key = deserialized_item["key"]
        r_server.delete(item_key)
        result = {"status": 1, "message": "Item Deleted", "item_key": item_key}

    except (Exception) as e:
        error = type(e)
        result = {"status": 0, "message": "Error", "error": error}

    return result


def get_items(redis_key):

    """
    Get item(s) in Redis

    Args:
        redis_key(str): string for 
        scan match
    """

    cursor_ = 0

    if redis_key:
        match_ = "{}*".format(redis_key)
    else:
        match_ = "*"

    try:
        cursor, keys_ = r_server.scan(cursor=cursor_, match=match_)

        byte_val_list = r_server.mget(keys_)
        val_list = []
        
        # Deserialize JSON object(s)
        for byte_val_ in byte_val_list:
            deserialized_val = json.loads(byte_val_)
            val_list.append(deserialized_val)

        result = val_list

    except (Exception) as e:
        error = type(e)
        result = {"status": 0, "message": "Error", "error": error}

    return result


if __name__ == "__main__":
    pass