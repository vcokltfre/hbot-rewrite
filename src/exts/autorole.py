from os import environ

from disnake import Member
from disnake.ext.commands import Cog

from src.impl.bot import Bot


class AutoRole(Cog):
    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        if member.guild.id != int(environ["GUILD_ID"]):
            return

        role = member.guild.get_role(int(environ["AUTO_ROLE_ID"]))

        if role is None:
            return

        await member.add_roles(role)


def setup(bot: Bot) -> None:
    bot.add_cog(AutoRole())
