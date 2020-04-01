from typing import List

from bin.characters.monsters import Monster
from bin.items import Item


class Fight:
    def __init__(self, players, enemies: List[Monster]):
        """
        :param players: List of Heros
        :param enemies: List of Monsters
        """
        self.players = players
        self.enemies = enemies
        self.loot: List[Item] = []
        names = enemies[0].name
        for enemy in enemies[1:-1]:
            names += ', ' + enemy.name
        if len(enemies) > 1:
            names += ' and ' + enemies[-1].name
        print('You started a fight with ' + names)

    def run(self) -> List[Item]:
        while len(self.enemies) > 0:
            enemy = self.enemies[0]
            hp = self.players[0].hp
            self.action(self.players[0])
            if enemy.is_dead():
                self.loot.append(enemy.loot())
                print(f'You defeated a {enemy.name}')
                self.enemies.remove(enemy)
            for i in self.enemies:
                self.players[0].get_hit(i.ad)
            if hp != self.players[0].hp:
                print(f'You are wounded and have {self.players[0].hp} hp')
        return self.end()

    def action(self, p):
        """
        :param p: Player
        """
        enemy = self.enemies[0]
        while True:
            inp = input('\nWhat do you want to do?\n[hit] an enemy\n[use] an item\n[run] out of the fight\n')
            if 'hit' in inp.lower():
                ad = p.ad
                if weapon := p.inventory.get(0):
                    ad = weapon.ad
                enemy.get_hit(ad)
                if not enemy.is_dead():
                    print(f'The {enemy.name} has {enemy.hp} hp left!')
                break
            elif 'use' in inp.lower():
                if p.use_item_menu():
                    break
            elif 'run' in inp.lower():
                # TODO implement this
                pass
            else:
                print("I couldn't understand you. Please try it again.")

    def end(self) -> List[Item]:
        print('All enemies are defeated!')
        return self.loot
