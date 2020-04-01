
class Character:
    def __init__(self, hp: int, ad: int, name: str, worth=None):
        self.hp = hp
        self.ad = ad
        self.name = name
        self.worth = worth

    def get_hit(self, ad: int):
        self.hp = self.hp - ad
        if self.hp <= 0:
            self.die()

    def is_dead(self):
        return self.hp <= 0

    def die(self):
        print(self.name + ' died')
