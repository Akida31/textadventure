from typing import List


class Map_blueprint:
    def __init__(self, name: str, file: str, fields_resolution: dict,
                 fields_enemy_probability: dict, drop_rate: dict, start: List[int],
                 sight_range: int):
        self.name = name
        self.file = file
        self.fields_resolution = fields_resolution
        self.fields_enemy_probability = fields_enemy_probability
        self.drop_rate = drop_rate
        self.start = start
