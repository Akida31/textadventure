from bin.items import Item


class Potion(Item):
    def __init__(self, weight, worth):
        Item.__init__(self, weight, worth)


class HealthPotion(Potion):
    def __init__(self, weight, worth, regenerated_health):
        Potion.__init__(self, weight, worth)
        self.regenerated_health = regenerated_health
        self.name = 'Healthpotion'


class Drink(HealthPotion):
    def __init__(self):
        HealthPotion.__init__(self, 0.5, 2, 20)
        self.name = 'Drink'


class Water(HealthPotion):
    def __init__(self):
        HealthPotion.__init__(self, 0.5, 1, 10)
        self.name = 'Water'