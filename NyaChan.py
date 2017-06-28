import sys
import discord
from discord.ext import commands
import asyncio
import role_ids
import configparser

config = configparser.ConfigParser()
config.read_file(open('settings.ini'))

startup_cogs = ['cog_rpg', 'cog_music', 'cog_misc']

bot = commands.Bot(command_prefix=config['Bot']['prefix'], description=config['Bot']['description'])

if len(sys.argv) == 2 and sys.argv[1] == 'dev':
    token = config['Bot']['token_dev']
else:
    token = config['Bot']['token_prod']

@bot.event
async def on_ready():
    print('######################################################')
    print('#                      Nya Chan                      #')
    print('######################################################')
    print('Bot User : ' + str(bot.user))
    url = await get_oauth_url()
    print('Oauth URL : ' + str(url))

async def get_oauth_url():
    data = await bot.application_info()
    return discord.utils.oauth_url(data.id)

#if __name__ == "__main__":
#    for cog in startup_cogs:
#        bot.load_extension(cog)

bot.run(token)

