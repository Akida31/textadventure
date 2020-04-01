import random
from typing import List

from bin.characters import Character
from bin.items import get_item, Item
from bin.items.potions import HealthPotion
from bin.items.weapons import Sword


class Monster(Character):
    def __init__(self, hp: int, ad: int, name: str, worth: int, the_loot: List[Item],
                 the_loot_weight: List[float]):
        Character.__init__(self, hp, ad, name, worth)
        self.worth = worth
        self.the_loot = the_loot
        self.the_loot_weight = the_loot_weight

    def loot(self) -> Item:
        if self.is_dead():
            item = random.choices(self.the_loot, self.the_loot_weight)[0]
            if isinstance(item, HealthPotion):
                return item
            elif isinstance(item, Sword):
                return item
            raise RuntimeError


class Goblin(Monster):
    def __init__(self, the_loot, the_loot_weight):
        Monster.__init__(self, 100, 10, 'Goblin', 1, the_loot, the_loot_weight)


class Ork(Monster):
    def __init__(self, the_loot, the_loot_weight):
        Monster.__init__(self, 300, 20, 'Ork', 3, the_loot, the_loot_weight)


def get_enemy(enemy: str, drop_rate: dict) -> Monster:
    """
    :param enemy: the name of the Monster
    :param drop_rate: the dict of the drop rate of the items
    :return: the Monster of which the name was given
    """
    classes = Monster.__subclasses__()
    if enemy not in [cls.__name__ for cls in classes]:
        raise IndexError(f'Monster {enemy} not found!')
    else:
        for cls in classes:
            if cls.__name__ == enemy:
                the_loot = []
                the_loot_weight = []
                drop_rate = drop_rate[enemy]
                for item in drop_rate:
                    the_loot.append(get_item(item))
                    the_loot_weight.append(drop_rate[item])
                return cls(the_loot, the_loot_weight)
