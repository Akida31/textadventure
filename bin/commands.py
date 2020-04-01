from inspect import signature

from bin.characters.hero import Player
from bin.text import show


def command(func):
    """
    This decorator calls the function with the right number of arguments.
    The argument order is:
        p - Player
        m - Map
    """
    def wrapper(*args, **kwargs):
        arglen = len(signature(func).parameters)
        if arglen > len(args):
            s = 's' if arglen - len(args) else ''
            raise TypeError(f'missing at least {arglen-len(args)} required positional argument{s}')
        try:
            func(*args[:arglen], **kwargs)
        except TypeError as error:
            if 'unexpected keyword argument' in error.__str__():
                func(*args[:arglen])
            else:
                raise error
    return wrapper


@command
def print_help():
    show('All commands are:')
    for cmd in command_description:
        show(cmd + ' - ' + command_description[cmd])


@command
def quit_game():
    show("You leave this world with a little smile in your face.")  # TODO ask for saving
    exit(0)


@command
def save(p):
    p.save('data/state.json')


@command
def use_item(p):
    p.use_item_menu()


@command
def get_inventory(p):
    items = p.get_inventory()
    if len(items) == 0:
        show('Your inventory is empty')
    elif len(items) == 1:
        show(f'Your inventory has 1 item:\n{items[0]}')
    else:
        show('All your items are:')
        for item in items:
            show(item)


@command
def hero_stats(p):
    inv = p.inventory.get_special_items()
    show(f'hp: {p.hp}')
    for item in inv:
        show(f'{item}: {inv[item]}')


@command
def get_area(p, m):
    p.get_area(m)


class move:
    @staticmethod
    @command
    def forward(p: Player, m):
        x, y = p.get_position()
        p.go(x, y - 1, m)

    @staticmethod
    @command
    def backward(p: Player, m):
        x, y = p.get_position()
        p.go(x, y + 1, m)

    @staticmethod
    @command
    def right(p: Player, m):
        x, y = p.get_position()
        p.go(x + 1, y, m)

    @staticmethod
    @command
    def left(p: Player, m):
        x, y = p.get_position()
        p.go(x - 1, y, m)


commands = {
    'help': print_help,
    'exit': quit_game,
    'quit': quit_game,
    'forward': move.forward,
    'right': move.right,
    'left': move.left,
    'backward': move.backward,
    'area': get_area,
    'w': move.forward,
    'a': move.left,
    's': move.backward,
    'd': move.right,
    'stats': hero_stats,
    'inventory': get_inventory,
    'save': save,
    'use': use_item
}

command_description = {
    'help': 'Shows help',
    'quit': 'Quits the game',
    'exit': 'Exits the game',
    'forward': 'Move your hero forward',
    'backward': 'Move your hero backward',
    'left': 'Move your hero left',
    'right': 'Move your hero right',
    'area': 'shows the map of the area around you',
    'save': 'Saves the game',
    'stats': 'shows your hero\'s stats',
    'inventory': 'Shows your inventory',
    'use': 'Use an item'
}
