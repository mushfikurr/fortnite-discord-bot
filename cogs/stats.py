import discord
from discord.ext.commands import Bot, Context, command, errors
from discord.ext import commands
from wrapper import tracker
from utils import methods
import main

class Stats:
    """ Stats cog. """
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def stats(self, ctx):
        """ Creates a group of commands, called Stats """
        if ctx.invoked_subcommand is None:
            await methods.create_help_embed(ctx, "Lookup", commands.MissingRequiredArgument)

    @stats.command()
    async def solo(self, ctx, user, platform):
        await tracker.embed_stats(ctx, user, platform, "Solo")
    
    @stats.command()
    async def duo(self, ctx, user, platform):
        await tracker.embed_stats(ctx, user, platform, "Duo")
    
    @stats.command()
    async def squad(self, ctx, user, platform):
        await tracker.embed_stats(ctx, user, platform, "Squad")
    
    @solo.error
    async def solo_on_error(self, ctx, error):
        await methods.create_help_embed(ctx, "Stats", error)

    @duo.error
    async def duo_on_error(self, ctx, error):
        await methods.create_help_embed(ctx, "Stats", error)

    @squad.error
    async def squad_on_error(self, ctx, error):
        await methods.create_help_embed(ctx, "Stats", error)

    @stats.error
    async def stats_on_error(self, ctx, error):
        await methods.create_help_embed(ctx, "Stats", error)

def setup(bot):
    bot.add_cog(Stats(bot))
