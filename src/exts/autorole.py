from os import environ

from disnake import Member
from disnake.ext.commands import Cog

from src.impl.bot import Bot


ROLE = int(environ["ROLE"])


class AutoRole(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        if member.guild.id != int(environ["GUILD_ID"]):
            return

        role = member.guild.get_role(ROLE)

        if role is None:
            return

        await member.edit(nick="h")
        await member.add_roles(role)

    @Cog.listener()
    async def on_ready(self) -> None:
        guild = self.bot.get_guild(int(environ["GUILD_ID"]))

        if guild is None:
            return

        for member in guild.members:
            if member.nick != "h":
                try:
                    await member.edit(nick="h")
                except Exception as e:
                    print(e)

            if ROLE not in member._roles:
                await member.add_roles(guild.get_role(ROLE))  # type: ignore


def setup(bot: Bot) -> None:
    bot.add_cog(AutoRole(bot))
