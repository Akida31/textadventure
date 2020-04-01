class Item:
    def __init__(self, weigth, worth):
        self.weight = weigth
        self.worth = worth
        self.name = '?ITEM?'

    def __str__(self):
        return self.name


def __all_subclasses(cls):
    """
    :param cls: class name
    :return: list of subclasses
    """
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in __all_subclasses(c)])


def get_item(item: str):
    """
    :param item: the name of the Item
    :return: the Item of which the name was given
    """
    found = False
    for cls in __all_subclasses(Item):
        if cls.__name__ == item:
            return cls()
    if not found:
        raise IndexError(f'Item {item} not found!')
