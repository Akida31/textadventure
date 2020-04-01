from bin.items import Item


class Weapon(Item):
    def __init__(self, weight, worth, ad):
        Item.__init__(self, weight, worth)
        self.ad = ad

    def get_ad(self):
        return self.ad


class Sword(Weapon):
    def __init__(self, weight, worth, ad):
        Weapon.__init__(self, weight, worth, ad)
        self.name = 'Sword'


class Longsword(Sword):
    def __init__(self):
        Sword.__init__(self, 2, 10, 60)
        self.name = 'Longsword'
