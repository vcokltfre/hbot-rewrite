from disnake.ext.commands import Bot as _Bot
from loguru import logger

from .status import StatusHeartbeater


class Bot(_Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._status = StatusHeartbeater()

    async def start(self, *args, **kwargs) -> None:
        self._status.run()

        await super().start(*args, **kwargs)

    async def on_connect(self) -> None:
        logger.info("Connected to the Discord Gateway.")

    async def on_ready(self) -> None:
        logger.info(f"READY event received, connected as {self.user} with {len(self.guilds)} guilds.")

    def load_extension(self, ext: str) -> None:
        super().load_extension(ext)

        logger.info(f"Loaded extension {ext}.")
