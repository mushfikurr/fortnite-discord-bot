import asyncio

import aiohttp
import async_timeout
import json
from discord import Embed
from utils import methods


def get_token():
    """ Retrives FortniteTracker API's token """
    with open('data/config.json', 'r', encoding='utf-8') as doc:
        config = json.load(doc)
    return config["trn-token"]


async def get_raw_json(nickname, platform):
    """ Fetches JSON file from API using aiohttp, returns a JSON file """
    url = f'https://api.fortnitetracker.com/v1/profile/{platform}/{nickname}'
    headers = {
        "TRN-Api-Key": get_token()
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with async_timeout.timeout(10):
                async with session.get(url) as response:
                    return await response.json()
        except asyncio.TimeoutError:
            print("Error in fetching JSON from API.")


class Player():
    """ A player class representing a request from the API """
    def __init__(self, nickname, platform):
        self.nickname = nickname
        self.platform = platform

    async def get_solo_stats(self):
        """ Returns a stats description for solo """
        stats = await get_raw_json(self.nickname, self.platform)
        print(f"Retrieving stats {self.nickname}:{self.platform}")
        try:
            win_ratio = stats["stats"]["p2"]["winRatio"]["displayValue"] + "%"
        except KeyError:
            win_ratio = "N/A"
        solo = {
            "epic-handle": stats["epicUserHandle"],
            "kills": stats["stats"]["p2"]["kills"]["displayValue"],
            "score": stats["stats"]["p2"]["score"]["displayValue"],
            "wins": stats["stats"]["p2"]["top1"]["displayValue"],
            "top10": stats["stats"]["p2"]["top10"]["displayValue"],
            "top25": stats["stats"]["p2"]["top25"]["displayValue"],
            "win-ratio": win_ratio,
            "kdr": stats["stats"]["p2"]["kd"]["displayValue"],
            "matches": stats["stats"]["p2"]["matches"]["displayValue"],
            "kill_per_match": stats["stats"]["p2"]["kpg"]["displayValue"],
            "score_per_match": stats["stats"]["p2"]["scorePerMatch"]
            ["displayValue"]
        }

        return solo

    async def get_duo_stats(self):
        """ Returns a stats description for duo """
        stats = await get_raw_json(self.nickname, self.platform)
        duo = {
            "epic-handle": stats["epicUserHandle"],
            "kills": stats["stats"]["p10"]["kills"]["displayValue"],
            "score": stats["stats"]["p10"]["score"]["displayValue"],
            "wins": stats["stats"]["p10"]["top1"]["displayValue"],
            "top10": stats["stats"]["p10"]["top10"]["displayValue"],
            "top25": stats["stats"]["p10"]["top25"]["displayValue"],
            "win-ratio": stats["stats"]["p10"]["winRatio"]["displayValue"],
            "kdr": stats["stats"]["p10"]["kd"]["displayValue"],
            "matches": stats["stats"]["p10"]["matches"]["displayValue"],
            "kill_per_match": stats["stats"]["p10"]["kpg"]["displayValue"],
            "score_per_match": stats["stats"]["p10"]["scorePerMatch"]
            ["displayValue"]
        }
        return duo

    async def get_squad_stats(self):
        """ Returns a stats description for squad """
        stats = await get_raw_json(self.nickname, self.platform)
        squad = {
            "epic-handle": stats["epicUserHandle"],
            "kills": stats["stats"]["p9"]["kills"]["displayValue"],
            "score": stats["stats"]["p9"]["score"]["displayValue"],
            "wins": stats["stats"]["p9"]["top1"]["displayValue"],
            "top10": stats["stats"]["p9"]["top10"]["displayValue"],
            "top25": stats["stats"]["p9"]["top25"]["displayValue"],
            "win-ratio": stats["stats"]["p9"]["winRatio"]["displayValue"],
            "kdr": stats["stats"]["p9"]["kd"]["displayValue"],
            "matches": stats["stats"]["p9"]["matches"]["displayValue"],
            "kill_per_match": stats["stats"]["p9"]["kpg"]["displayValue"],
            "score_per_match": stats["stats"]["p9"]["scorePerMatch"]
            ["displayValue"]
        }
        return squad


async def embed_stats(ctx, nickname, platform, mode):
        """ Generates an embed with stats. Takes context, epic username,
        platform, and the mode you are generating the stats for. """
        player = Player(nickname, platform)
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
        kill_per_match = s["kill_per_match"]
        score_per_match = s["score_per_match"]
        time = methods.get_time()
        author = ctx.author.display_name
        embed_description = (f"These are statistics accumulated over"
                             "the lifetime of the account")
        embed_title = f"{mode}, generated for {handle}"
        embed = Embed(
            title=embed_title, description=embed_description, color=0xff0000)
        embed.set_author(name="Statistics",
                         icon_url="https://i.imgur.com/tQOWoEv.png")
        win_field_value = (f"Wins: {wins}\n"
                           f"Win Percentage: {win_ratio}\n"
                           f"Top 10: {top10}\n"
                           f"Top 25: {top25}")
        embed.add_field(name="Positions", value=win_field_value, inline=True)
        combat_field_value = (f"Kills: {kills}\n"
                              f"Kill Per Game: {kill_per_match}\n"
                              f"Kill/Death Ratio: {kdr}")
        embed.add_field(name="Combat", value=combat_field_value)
        score_field_value = (f"Overall Score: {score}\n"
                             f"Score Per Match: {score_per_match}")
        embed.add_field(name="Score", value=score_field_value)
        embed.set_footer(text=f"Generated by @{author}, {time}")
        await ctx.send(embed=embed)
