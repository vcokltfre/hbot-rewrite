from os import environ

from disnake import Intents

from . import Bot


def main() -> None:
    intents = Intents.default()
    intents.members = True

    bot = Bot(intents=intents)

    for ext in [
        "src.exts.automod",
        "src.exts.autorole",
    ]:
        bot.load_extension(ext)

    bot.run(environ["TOKEN"])


main()
