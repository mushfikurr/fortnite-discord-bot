import discord
from discord.ext.commands import Bot, Context, command, errors
from discord.ext import commands
from wrapper import tracker
import main
from utils import methods
from wrapper import lookup

class Lookup:
    """ Stats cog. """
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def lookup(self, ctx):
        """ Creates a group of commands, called Lookup """
        if ctx.invoked_subcommand is None:
            await methods.create_help_embed(ctx, "Lookup", commands.MissingRequiredArgument)
    
    @lookup.command()
    async def weapon(self, ctx, *, weapon_name):
        await lookup.handle_command(ctx, weapon_name)
    
    @lookup.error
    async def lookup_error(self, ctx, error):
        await methods.create_help_embed(ctx, "Lookup", error)

    @weapon.error
    async def lookup_weapon_error(self, ctx, error):
        await methods.create_help_embed(ctx, "Lookup", error)

def setup(bot):
    bot.add_cog(Lookup(bot))
