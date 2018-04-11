import bs4 as bs

import async_timeout
import asyncio
import aiohttp
import difflib
from utils import weapondata
from utils import methods
import discord

async def get_html(url):
    """ Retrieves HTML of the database """
    async with aiohttp.ClientSession() as session:
        async with async_timeout.timeout(10):
            async with session.get(url) as response:
                return await response.text()

# Scrapes all links
async def get_all_weapon_links():
    url = "https://db.fortnitetracker.com/weapons"
    soup = bs.BeautifulSoup(await get_html(url), "lxml")
    links = []
    for weapon in soup.find_all('tr'):
        links.append(weapon.find('a'))
    weapon_links = {}
    for link in links:
        if link is not None:
            print("Returning all weapon links")
            href = link.get('href')
            #Hardcoded value [9:]
            weapon_name = str(href)[9:]
            weapon_links[weapon_name] = href
    return weapon_links

# Gets specific weapon link
async def get_weapon_link(weapon_name):
    links = await get_all_weapon_links()
    for name in links.keys():
        if weapon_name == name:
            return links[name]
        

# Scrapes for stats for weapon_name, requires a weapon_dict -> Dict
async def scrape_for_weapon(weapon_name):
    weapon_stats = {}
    weapon_links = await get_all_weapon_links()
    name_formatted = weapon_name.lower().replace(" ", "-")
    raw = await get_html("https://db.fortnitetracker.com/" + weapon_links[name_formatted])
    new_soup = bs.BeautifulSoup(raw, "lxml")
    parent = new_soup.find("h3", text="Quick information").parent
    grandfather = parent.parent
    img_url = grandfather.find("div", class_="col-md-2")
    img = img_url.find("img")
    print(f"Returning scraped info img: {str(img)}")
    item_info = grandfather.find("div", class_="panel-item-info")
    stats = item_info.find_all("tr")
    for tr in stats:
        td_list = []
        for td in tr.find_all("td"):
           text = td.text
           td_list.append(text) 
        weapon_stats[td_list[0]] = td_list[1]
    print(f"Returning weapon_stats dict {weapon_stats}")
    wep_link = await get_weapon_link(name_formatted)
    weapon_stats["wepUrl"] = "https://db.fortnitetracker.com" + wep_link
    weapon_stats["imgUrl"] = "https://db.fortnitetracker.com" + img.get('src')
    return weapon_stats

# Lookup weapon in database (weapon="(x-y-z-rarity)")
async def get_weapon_stats(weapon_name):
    frmtd_wep = weapon_name.lower().replace(" ", "-")
    print(frmtd_wep)
    wep_links = await get_all_weapon_links()
    print(wep_links)
    if frmtd_wep in wep_links.keys():
        if weapondata.lookup_data(frmtd_wep) is not None:
            print("Apparently the lookup is NOT NONE")
            return weapondata.lookup_data(frmtd_wep)
        else:
            print(f"This should actually execute well done if it does {weapon_name}")
            weapon_stats = await scrape_for_weapon(weapon_name)
            # Creates a record of a new weapon that it couldn't find in query.
            print(f"[{methods.get_today_date()}] Creating new record {weapon_name}")
            weapondata.input_data(frmtd_wep, weapon_stats["Damage"], weapon_stats["Critical Hit Chance"], weapon_stats["Critical Hit Damage"], weapon_stats["Fire Rate"],
            weapon_stats["Magazine Size"], weapon_stats["Range"], weapon_stats["Durability"], weapon_stats["Reload Time"], weapon_stats["Ammo Cost"],
            weapon_stats["Impact"], weapon_stats["wepUrl"], weapon_stats["imgUrl"])
            return weapondata.lookup_data(frmtd_wep)
    else:
        print("Couldnt find in links, so did not scrape")
        return None

# Format weapon name

# Creates an embed for weapon stats
async def embed_weapon_stats(ctx, arguments):
    weapon = await get_weapon_stats(arguments)
    if weapon is None:
        ctx.send("We couldnt find that weapon.")
    else:
        if weapon["Rarity"] == "common":
            embed_colour = 0xb0b0b0
        elif weapon["Rarity"] == "uncommon":
            embed_colour = 0x54ad50
        elif weapon["Rarity"] == "rare":
            embed_colour = 0x5066ad
        elif weapon["Rarity"] == "epic":
            embed_colour = 0x651786
        elif weapon["Rarity"] == "legendary":
            embed_colour = 0xffdb34
        else:
            embed_colour = 0xffffff
        wep_name = weapon["Name"]
        damage = weapon["Damage"]
        crit_chance = weapon["Critical Hit Chance"]
        crit_dmg = weapon["Critical Damage"]
        fire_rate = weapon["Fire Rate"]
        mag_size = weapon["Magazine Size"]
        range = weapon["Range"]
        durability = weapon["Durability"] 
        reload_time = weapon["Reload Time"]
        ammo_cost = weapon["Ammo Cost"]
        impact = weapon["Impact"]
        thumbnail = weapon["imgUrl"]
        wep_url = weapon["wepUrl"]
        description = f"""
**Damage:** {damage}
**Critical Damage Chance:** {crit_chance}
**Critical Damage:** {crit_dmg}
**Fire Rate:** {fire_rate}
**Magazine Size:** {mag_size}
**Range:** {range}
**Durability:** {durability}
**Reload Time:** {reload_time}
**Ammo Cost:** {ammo_cost}
**Impact:** {impact}
    """
        embed=discord.Embed(title=wep_name, url=wep_url, description=description, color=embed_colour)
        embed.set_thumbnail(url=thumbnail)
        await ctx.send(embed=embed)


# Handles searches
async def handle_command(ctx, arguments):
    if get_weapon_stats(arguments) is not None:
        await embed_weapon_stats(ctx, arguments)
    else:
        related_searches = difflib.get_close_matches(arguments, await get_all_weapon_links().keys(), 4, 0.4)
        print("We couldn't find that weapon. Did you mean.. ")
        for search in related_searches:
            search = search.replace("-", " ")
            print(search)