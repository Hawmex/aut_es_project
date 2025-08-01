import textwrap


def print_headline(message: str, char: str = "-", width: int = 80):
    lines = textwrap.wrap(message, width)

    print(char * width)
    print("\n".join(lines) if len(lines) > 1 else lines[0].center(width))
    print(char * width)
