def item_generator(num_of_items):

    """ 
    Generate a list of items for Redis insertion 

    Args: 
        num_of_items(int): number of items 
        you want to make
    """

    generated_items = []

    for i in range(0, num_of_items):

        item_dict = {
            "key": "000{}".format(i),
            "details": "Item #{} Details".format(i),
        }
        generated_items.append(item_dict)

    return generated_items