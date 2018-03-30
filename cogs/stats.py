import discord
from discord.ext.commands import Bot, Context, command, errors
from discord.ext import commands
from wrapper import tracker
import main

async def embed_stats(ctx, nickname, platform, mode):
    """ Generates an embed with stats. Takes context, epic username, platform, and the mode you are generating the stats for. """
    player = tracker.Player(nickname, platform)
    if mode == "Solo":
        s = await player.get_solo_stats()
    elif mode == "Duo":
        s = await player.get_duo_stats()
    elif mode == "Squad":
        s = await player.get_squad_stats()
    handle = s["epic-handle"]
    score = s["score"]
    wins = s["wins"]
    top10 = s["top10"]
    top25 = s["top25"]
    kdr = s["kdr"]
    win_ratio = s["win-ratio"]
    kills = s["kills"]
    time_per_match = s["time_per_match"]
    kill_per_match = s["kill_per_match"]
    score_per_match = s["score_per_match"]
    embed_description = f"""These statistics are accumulated over the lifetime of the account.\n
**Wins**: {wins}\n
**Win ratio**: {win_ratio}\n
**Top 10**: {top10}\n
**Top 25**: {top25}\n
**KD**: {kdr}\n
**Kills**: {kills}\n
**Kills per match**: {kill_per_match}\n
**Score**: {score}\n
**Average time survived**: {time_per_match}\n
**Average score per match**: {score_per_match}\n"""
    embed=discord.Embed(title=f"Generated for {handle}", description=embed_description, color=0xff0000)
    embed.set_author(name=mode)
    await ctx.send(embed=embed)


async def embed_help(ctx, error):
    """ Generates an embed with help/troubleshooting. Takes CTX, and discord generated error. """
    command = ctx.command
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(title="Incorrect arguments", description=f"!{command} (solo/duo/squad/lifetime) (username) (psn/xbl/pc)", color=0xff8000)
        embed.set_footer(text="To view all commands, type !help")
    elif isinstance(error, TypeError):
        embed=discord.Embed(title="Could not find account", description=f"Ensure your PSN/XBL account is linked with Epic Games. For more information type !linking.", color=0xff8000)
        embed.set_footer(text="To view all commands, type !help")
    elif isinstance(error, KeyError):
        embed=discord.Embed(title="Could not find account", description=f"Ensure your PSN/XBL account is linked with Epic Games. For more information type !linking.", color=0xff8000)
        embed.set_footer(text="To view all commands, type !help")
    else:
        print("ERROR: " + str(error))
        embed=discord.Embed(title="There was a problem processing your request", description=f"!{command} (modes) (username) (platforms)", color=0xff8000)
        embed.add_field(name="Modes", value="solo/duo/squad/lifetime", inline=True)
        embed.add_field(name="Platforms", value="pc/xbl/psn", inline=True)
        embed.add_field(name="Username", value="You must have an Epic Account associated with your XBOX/PSN account. To find out more, type !link", inline=False)
        embed.add_field(name="Troubleshooting", value="If all arguments are correct and it is still not working, contact an admin.", inline=False)
        embed.set_footer(text="To view all commands, type !help")
         
    await ctx.send(embed=embed) 


class Stats:
    """ Stats cog. """
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def stats(self, ctx):
        """ Creates a group of commands, called Stats """
        if ctx.invoked_subcommand is None:
            await embed_help(ctx.channel, ctx.command.name)

    @stats.command()
    async def solo(self, ctx: Context, user, platform):
        channel = ctx.channel
        await embed_stats(channel, user, platform, "Solo")
    
    @stats.command()
    async def duo(self, ctx: Context, user, platform):
        channel = ctx.channel
        await embed_stats(channel, user, platform, "Duo")
    
    @stats.command()
    async def squad(self, ctx: Context, user, platform):
        channel = ctx.channel
        await embed_stats(channel, user, platform, "Squad")
    
    @solo.error
    async def solo_on_error(self, ctx, error):
        await embed_help(ctx, error)

    @duo.error
    async def duo_on_error(self, ctx, error):
        await embed_help(ctx, error)

    @squad.error
    async def squad_on_error(self, ctx, error):
        await embed_help(ctx, error)

    @stats.error
    async def stats_on_error(self, ctx, error):
        await embed_help(ctx, error)

def setup(bot):
    bot.add_cog(Stats(bot))
