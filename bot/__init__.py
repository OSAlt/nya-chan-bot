import discord
import logging
from discord.ext import commands
from .context import CommandContext
from .config import Bot as BotConfig

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='debug.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class BotBase(commands.Bot):
    def __init__(self, *args, **kwargs):
        kwargs.update(command_prefix=BotConfig.token)
        super().__init__(*args, **kwargs)

    async def process_commands(self, message):
        if message.author.bot:
            return

        ctx = await self.get_context(message, cls=CommandContext)
        await self.invoke(ctx)

    async def on_ready(self):
        print('######################################################')
        print('#                      Nya Chan                      #')
        print('######################################################')

        print(f'Discord.py version : {discord.__version__}')
        print(f'Bot User : {self.user}')

        app_info = await self.application_info()
        self.owner_id = app_info.owner.id
        print(f'Bot Owner : {app_info.owner.id}')

        url = discord.utils.oauth_url(app_info.id)
        print(f'Oauth URL : {url}')