import discord
from discord.ext.commands import Bot, Context, command, errors
from discord.ext import commands
from wrapper import tracker
import main
from wrapper import lookup

class Lookup:
    """ Stats cog. """
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def lookup(self, ctx):
        """ Creates a group of commands, called Lookup """
        if ctx.invoked_subcommand is None:
            await ctx.send("lol wut")
    
    @lookup.command()
    async def weapon(self, ctx, *, weapon_name):
        await lookup.handle_command(ctx, weapon_name)
        print(weapon_name)

def setup(bot):
    bot.add_cog(Lookup(bot))
