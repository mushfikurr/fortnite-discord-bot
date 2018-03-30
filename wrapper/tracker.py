import os

import asyncio

import aiohttp
import async_timeout
import json

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
            "score_per_match": stats["stats"]["p2"]["scorePerMatch"]["displayValue"],
            "time_per_match": stats["stats"]["p2"]["avgTimePlayed"]["displayValue"],
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
            "score_per_match": stats["stats"]["p10"]["scorePerMatch"]["displayValue"],
            "time_per_match": stats["stats"]["p10"]["avgTimePlayed"]["displayValue"],
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
            "score_per_match": stats["stats"]["p9"]["scorePerMatch"]["displayValue"],
            "time_per_match": stats["stats"]["p9"]["avgTimePlayed"]["displayValue"],
        }
        return squad 