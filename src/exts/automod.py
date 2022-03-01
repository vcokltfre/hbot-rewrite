from os import environ

from disnake import AllowedMentions, Message, TextChannel
from disnake.ext.commands import Cog
from disnake.http import Route

from src.impl.bot import Bot

CHANNELS = [int(c) for c in environ["CHANNELS"].split(";")]
LOGS = int(environ["LOGS"])


class AutoMod(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.channel.id not in CHANNELS:
            return

        if not isinstance(message.channel, TextChannel):
            return

        if (
            message.stickers
            or message.attachments
            or message.embeds
            or message.components
            or message.content != message.channel.name
        ):
            await message.delete()

            lc: TextChannel = self.bot.get_channel(LOGS)  # type: ignore

            if lc:
                await lc.send(
                    f"Message from {message.author.mention} has been automatically deleted in {message.channel.mention}:\n\n{message.content[:1800]}",
                    allowed_mentions=AllowedMentions(users=False, roles=False, everyone=False),
                )

    @Cog.listener()
    async def on_raw_message_edit(self, payload: dict) -> None:
        if payload["channel_id"] not in CHANNELS:
            return

        message_id = payload["message_id"]
        channel_id = payload["channel_id"]

        await self.bot.http.request(
            Route(
                "DELETE",
                "/channels/{channel_id}/messages/{message_id}",
                channel_id=channel_id,
                message_id=message_id,
            )
        )


def setup(bot: Bot) -> None:
    bot.add_cog(AutoMod(bot))
