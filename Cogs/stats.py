import discord
from discord.ext import commands
import pymysql
import role_ids
from __main__ import config

class Stats():
    """Welcomes new members to the server via private message"""
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if not message.content.startswith(self.bot.command_prefix):
            guild = message.guild
            author = message.author
            channel = message.channel
            if not channel is None:
                connection = pymysql.connect(host=config['Database']['host'], user=config['Database']['user'], password=config['Database']['password'], db=config['Database']['database'], charset='utf8')
                cursor = connection.cursor()
                cursor.execute("""SELECT id FROM statistics_global WHERE id_server = %s AND id_user = %s AND id_channel = %s""", (guild.id, author.id, channel.id))
                rows = cursor.fetchall()
                if len(rows) == 0:
                    cursor.execute("""INSERT INTO statistics_global (id, id_server, id_user, id_channel, msg_count) VALUES (null, %s, %s, %s, 1)""", (guild.id, author.id, channel.id))
                    connection.commit()
                else:
                    row_id = rows[0][0]
                    cursor.execute("""UPDATE statistics_global SET msg_count = msg_count + 1 WHERE id = %s""", (row_id))
                    connection.commit()
                connection.close()

def Stats(bot):
    cog = Welcome(bot)
    bot.add_listener(cog.member_join, "on_member_join")
    bot.add_cog(cog)

