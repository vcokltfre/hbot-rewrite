from os import environ

from . import Bot


def main() -> None:
    bot = Bot()

    for ext in [
        "src.exts.automod",
        "src.exts.autorole",
    ]:
        bot.load_extension(ext)

    bot.run(environ["TOKEN"])


main()
