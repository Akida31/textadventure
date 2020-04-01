from importlib import import_module, util
import random
from typing import List, Tuple

from bin.characters.fight import Fight
from bin.characters.monsters import get_enemy
from bin.text import show


class Map:
    def __init__(self, fields: List[str], resolution: dict, enemies: dict, drop_rate: dict,
                 start: Tuple[int, int] = (0, 0)):
        self.fields = fields
        self.start = start
        self.resolution = resolution
        self.enemies = enemies
        self.drop_rate = drop_rate

    def get_size(self) -> Tuple[int, int]:
        return len(self.fields[0]), len(self.fields)

    def get_block(self, left: int = None, right: int = None,
                  top: int = None, bottom: int = None) -> List[List[str]]:
        if left is None:
            left = 0
            right = self.get_size()[0] - 1
            top = 0
            bottom = self.get_size()[1] - 1
        if (left < 0 or left > right or right > self.get_size()[0] or
                top < 0 or top > bottom or bottom > self.get_size()[1]):
            raise IndexError
        tiles = []
        for y in range(top, bottom+1):
            tiles.append([])
            for x in range(left, right+1):
                tiles[len(tiles) - 1].append(self.get_field(x, y))
        return tiles

    def get_field(self, x: int, y: int) -> str:
        if ((x < 0) or (x >= self.get_size()[0]) or
                (y < 0) or (y >= self.get_size()[1])):
            raise IndexError
        field = self.resolution[self.fields[y][x]]
        return field

    def go(self, x, y, p):
        field = self.fields[y][x]
        if field not in self.enemies:
            return
        enemies = self.enemies[field]
        enemy_list: str = random.choices(list(enemies.keys()), [enemies[k] for k in enemies])[0]
        if enemy_list == 'None':
            return
        enemies = []
        for enemy in enemy_list.split(' '):
            enemies.append(get_enemy(enemy, self.drop_rate))
        # random.choices returns a list, so we have to get the first value
        f = Fight([p], enemies)
        loot = f.run()
        show('You got:')
        for item in loot:
            show(item)
            p.get_item(item)


def load_map(file: str, cwd: str = '') -> Map:
    m = import_module(f'maps.{file}').the_map
    x: int = m.start[0]
    y: int = m.start[1]
    fields = []
    with open(f'{cwd}maps/{m.file}') as f:
        for line in f.readlines():
            fields.append(line.strip().replace('\n', ''))
    m2 = Map(fields, m.fields_resolution, m.fields_enemy_probability, m.drop_rate, (x, y))
    # TODO sight range
    return m2
