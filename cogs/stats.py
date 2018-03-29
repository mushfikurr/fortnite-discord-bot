import discord
from discord.ext.commands import Bot, Context, command, errors
from wrapper import tracker

async def embed_stats(channel, nickname, platform):
    player = tracker.Player(nickname, platform)
    s = await player.get_solo_stats()
    handle = s["epic-handle"]
    score = s["score"]
    wins = s["wins"]
    top10 = s["top10"]
    top25 = s["top25"]
    kdr = s["kdr"]
    win_ratio = s["win-ratio"]
    kills = s["kills"]
    time_per_match = s["time_per_match"]
    score_per_match = s["score_per_match"]
    solo_description = f"""These statistics are accumulated over the lifetime of the account.\n
**Wins**: {wins}\n
**Win ratio**: {win_ratio}\n
**Top 10**: {top10}\n
**Top 25**: {top25}\n
**KD**: {kdr}\n
**Kills**: {kills}\n
**Average time survived**: {time_per_match}\n
**Average score per match**: {score_per_match}\n"""
    embed=discord.Embed(title=f"Generated for {handle}", description=solo_description, color=0xff0000)
    embed.set_author(name="Solo")
    '''
    embed.add_field(name="Solo", value="|", inline=True)
    embed.add_field(name="Score", value=score, inline=True)
    embed.add_field(name="Wins", value=f"{wins} ({win_ratio})", inline=True)
    embed.add_field(name="|", value="|", inline=True)
    embed.add_field(name="Top 10", value=top10, inline=True)
    embed.add_field(name="Top 25", value=top25, inline=True)
    embed.add_field(name="|", value="|", inline=True)
    embed.add_field(name="K/D", value=kdr, inline=True)
    embed.add_field(name="Kills", value=kills, inline=True)
    embed.add_field(name="|", value="|", inline=True)
    embed.add_field(name="Average Time Played", value=time_per_match, inline=True)
    embed.add_field(name="Score Per Match", value=score_per_match, inline=True)
    '''
    await channel.send(embed=embed)


async def embed_help(channel):
    embed=discord.Embed(title="Something went wrong!", description="!stats {username} {psn/xbox/pc} {current/lifetime/overall}", color=0xff8000)
    embed.add_field(name="Platforms", value="pc/xbl/psn", inline=True)
    embed.add_field(name="Username", value="You must have an Epic Account associated with your XBOX/PSN account. To find out more, type !link", inline=False)
    embed.add_field(name="Troubleshooting", value="If all arguments are correct and it is still not working, contact an admin.", inline=False)
    embed.set_footer(text="To view all commands, type !help")
    await channel.send(embed=embed) 


class Stats:
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def statsolo(self, ctx: Context, user, platform):
        channel = ctx.channel
        await embed_stats(channel, user, platform)
        
    @statsolo.error
    async def stats_on_error(self, ctx, error):
        await embed_help(ctx.channel)

def setup(bot):
    bot.add_cog(Stats(bot))
