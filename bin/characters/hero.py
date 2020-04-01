import json
from typing import Dict, List, Tuple

from bin.characters import Character
from bin.items import Item
from bin.items.potions import HealthPotion
from bin.items.weapons import Sword
from bin.themap import Map, load_map
from bin.text import get_input, show


class Player(Character):
    def __init__(self, name: str, map_name: str, level: int):
        Character.__init__(self, 400, 50, name)
        self.max_hp = 400
        self.hp = self.max_hp
        self.x = 0
        self.y = 0
        self.level = level
        self.map = map_name
        self.inventory = Inventory()

    def set_position(self, x: int, y: int, m: Map) -> bool:
        length, height = m.get_size()
        if 0 < x < length - 1:
            valid = True
        else:
            valid = False
        if not (0 < y < height - 1):
            valid = False
        if valid:
            self.x = x
            self.y = y
        return valid

    def go(self, x: int, y: int, m: Map):
        if not self.set_position(x, y, m):
            # TODO put here some messages for water and so on
            show("There are huge mountains you can't pass!!")
            return
        m.go(x, y, self)
        self.get_area(m)

    def get_area(self, m):
        x = self.x
        y = self.y
        fields = m.get_block(x - 1, x + 1, y - 1, y + 1)
        row_num = 0
        for row in fields:
            col_num = 0
            show('\n----------------------------------------', end='\n| ')
            for col in row:
                if col_num == 1 and row_num == 1:
                    show(self.name + " " * (10 - len(self.name)), end=' | ')
                else:
                    c = col + ' ' * (10 - len(col))
                    show(c, end=' | ')
                col_num += 1
            row_num += 1
        show('\n----------------------------------------')

    def get_item(self, item: Item):
        if {'error': 'inventory is full'} == self.inventory.get_item(item):
            show('Your inventory is full!')
            show(f"You can't take {item} with you")

    def get_inventory(self):
        return self.inventory.get()

    def get_position(self) -> Tuple[int, int]:
        return self.x, self.y

    def set_hp(self, hp: int):
        if 0 < hp <= self.max_hp:
            self.hp = hp

    def die(self):
        exit('Wasted. Try again.')

    def rest(self):
        self.hp = self.max_hp

    def export(self) -> json:
        res = {'name': self.name, 'x': self.x, 'y': self.y,
               'hp': self.hp, 'map': self.map,
               'lvl': self.level}
        return json.dumps(res)

    def save(self, file: str):
        with open(file, 'w') as f:
            f.write(self.export())

    def use_item_menu(self) -> bool:
        """
        Ask the player which item should be used.
        Returns if an item was used
        """
        # TODO function accepts command line args, tests for right item
        items = self.get_inventory()
        if len(items) == 0:
            show('Your inventory is empty')
        elif len(items) == 1:
            if 'y' in get_input(f'Do you want to use {items[0]} [y/n]? '):
                self.use_item(items[0])
                return True
        else:
            while True:
                show('All your items are:')
                for i in range(len(items)):
                    show(f'{i + 1}: {items[i]}')
                inp = get_input('Which item you want to use?\nLeave it empty if you don\'t want to use any: ')
                try:
                    inp = int(inp)
                except ValueError:
                    break
                if 0 < inp <= len(items):
                    self.use_item(items[inp - 1])
                    return True
        return False

    def use_item(self, item: Item):
        if isinstance(item, HealthPotion):
            hp = self.hp
            self.set_hp(self.hp + item.regenerated_health)
            show(f'You regenerated {self.hp - hp} health')
            res = self.inventory.remove(item)
            if 'ok' not in res:
                raise IndexError
        elif isinstance(item, Sword):
            self.inventory.swap(0, self.inventory.index(item))
            show(f'You use now a sword with {item.ad} ad as your weapon')
        else:
            raise NotImplementedError


def import_hero(file: str) -> Tuple[Map, Player]:
    with open(file) as f:
        imp = json.loads(f.read())
    p = Player(imp['name'], imp['map'], imp['lvl'])
    m = load_map(p.map)
    p.set_position(imp['x'], imp['y'], m)
    p.set_hp(imp['hp'])
    return m, p


class Inventory:
    """the class for the inventory of the hero
    includes a total of 30 items and the first 10 spots are reserved for special items:
    1. Weapon
    """

    def __init__(self):
        self.items = [None for i in range(10)]
        self.special_items = ['weapon']

    def get_special_items(self) -> Dict[str, Item]:
        res = {}
        for i in range(10):
            if self.items[i] is not None:
                res[self.special_items[i]] = self.items[i]
        return res

    def get(self, index=None) -> List[Item] or Item:
        if index is not None:
            return self.items[index]
        res = []
        for item in self.items:
            if item:
                res.append(item)
        return res

    def get_item(self, item: Item) -> dict:
        if len(self.items) >= 30:
            return {'error': 'inventory is full'}
        else:
            self.items.append(item)
            return {'ok': 'success'}

    def remove(self, item: Item) -> dict:
        for i in self.items:
            if type(item) == type(i):
                self.items.remove(i)
                return {'ok': 'success', 'item': item}
        return {'error': 'item not found'}

    def swap(self, index1: int, index2: int):
        if (0 <= index1 < len(self.items)) and (0 <= index2 < len(self.items)):
            self.items[index1], self.items[index2] = self.items[index2], self.items[index1]
            return True
        return False

    def index(self, item: Item):
        if item not in self.items:
            raise IndexError  # PRODUCTION: uncaught error, should be fixed
            # return -1
        for i in range(len(self.items)):
            if self.items[i] == item:
                return i
