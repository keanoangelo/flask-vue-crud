from redis import Redis
import json
from utils import item_generator, func_iterator

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
        json_dict = json.dumps(item_dict)
        item_key = item_dict["key"]
        r_server.set(item_key, json_dict)
        result = {"status": 1, "message": "Item Created", "item": item_dict}

    # TODO: Change this to more suitable catch
    except (Exception) as e:
        error = type(e)
        result = {"status": 0, "message": "Error", "error": error}

    return result


def delete_item(item_):

    """ 
    Delete item in Redis

    Args: 
        item_(dictionary): item 
        to be deleted in Redis
    """

    try:
        item_key = item_["key"]
        r_server.delete(item_key)
        result = {"status": 1, "message": "Item Deleted", "item_key": item_key}

    # TODO: Change this to more suitable catch
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

    # TODO: Change this hardcoded cursor
    cursor_ = 0
    match_ = "{}*".format(redis_key)

    try:
        
        cursor, keys_ = r_server.scan(cursor=cursor_, match=match_)

        r_response = r_server.mget(keys_)
        json_val_list = []
        
        # Jsonify object(s)
        for val_ in r_response:
            json_val = json.loads(val_)
            json_val_list.append(json_val)

        result = json_val_list

    # TODO: Change this to more suitable catch
    except (Exception) as e:
        error = type(e)
        result = {"status": 0, "message": "Error", "error": error}

    return result


if __name__ == "__main__":
    pass