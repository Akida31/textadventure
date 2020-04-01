
# TODO


def translate(text: str) -> str:
    # TODO read language from file
    return text


def decorate(text: str) -> str:
    return text


def show(text, end='\n'):
    print(decorate(translate(text.__str__())), end=end)


def get_input(text: str = '') -> str:
    show(text, end='')
    return input()
