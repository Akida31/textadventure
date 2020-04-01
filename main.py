import os
from typing import Tuple

from bin.characters.hero import import_hero, Player
from bin.commands import commands
from bin.themap import Map, load_map
from bin.text import get_input, show

# if you want to use this in production, look for all lines in all files with PRODUCTION in it


def new() -> Tuple[Map, Player]:
    while True:
        name = get_input('Please enter your name: ')
        if len(name) < 11:
            break
        show('Your name should be shorter than 11 letters')
    player = Player(name, 'start', 0)
    m = load_map('start', cwd)
    x, y = m.start
    player.set_position(x, y, m)
    return m, player


def load() -> Tuple[Map, Player]:
    #  TODO different game states, multiple games saved
    file = 'data/state.json'
    if os.path.exists(file):
        return import_hero(file)
    raise FileNotFoundError


def main():
    while True:
        inp = get_input("[Load] | [New] ").lower()
        if 'load' in inp:
            m, p = load()
            break
        elif 'new' in inp:
            m, p = new()
            break
        show('I couldnt understand you, please repeat your answer!')
    show(f'\nHello {p.name},\nWelcome to our wonderful world!\nYou are here:')
    p.get_area(m)
    show("(type help to see your abilities)\n")
    while True:
        try:
            command = get_input("\n>").lower().split(" ")
            if command[0] in commands:
                commands[command[0]](p, m)
            else:
                show("You run around in circles and don't know what to do.")
        except KeyboardInterrupt:
            show('Please exit normally with the command exit...')
            exit(1)  # PRODUCTION: remove this


if __name__ == '__main__':
    cwd = os.getcwd().replace('\\', '/') + '/'  # TODO Load this from file
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    try:
        main()
    except RuntimeError as e:  # PRODUCTION  remove "as e"
        raise e  # PRODUCTION  remove this line
        show('Runtime error. Exiting...')
        exit(0)
