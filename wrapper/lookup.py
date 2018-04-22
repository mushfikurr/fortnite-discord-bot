import bs4 as bs

import async_timeout
import aiohttp
import difflib
from utils import weapondata
from utils import methods
from discord import Embed


async def get_html(url):
    """ Retrieves HTML of a webpage """
    async with aiohttp.ClientSession() as session:
        async with async_timeout.timeout(10):
            async with session.get(url) as response:
                return await response.text()


async def get_all_weapon_links():
    """ Gets all weapons that it can find on the database
    returning their links """
    url = "https://db.fortnitetracker.com/weapons"
    soup = bs.BeautifulSoup(await get_html(url), "lxml")
    links = []
    for weapon in soup.find_all('tr'):
        links.append(weapon.find('a'))
    weapon_links = {}
    for link in links:
        if link is not None:
            href = link.get('href')
            weapon_name = str(href)[9:]  # length of weapons/
            weapon_links[weapon_name] = href
    return weapon_links


async def get_weapon_link(weapon_name):
    """ Returns a specific weapons sub domain """
    links = await get_all_weapon_links()
    for name in links.keys():
        if weapon_name == name:
            return links[name]


async def convert_to_storable_name(weapon_name):
    """ Converts a string from a WeApOn X to a_weapon_x """
    formatted = weapon_name.lower().replace(" ", "-")
    return formatted


async def scrape_for_weapon(weapon_name):
    """ Scrapes for a weapon on db.fortnitetracker.com if it exists in the
    links. Returns a dictionary of weapon stats """
    weapon_stats = {}
    weapon_links = await get_all_weapon_links()
    name_formatted = await convert_to_storable_name(weapon_name)
    weapon_link = weapon_links[name_formatted]
    raw = await get_html("https://db.fortnitetracker.com/" + weapon_link)
    new_soup = bs.BeautifulSoup(raw, "lxml")
    parent = new_soup.find("h3", text="Quick information").parent
    grandfather = parent.parent
    img_url = grandfather.find("div", class_="col-md-2")
    img = img_url.find("img")
    item_info = grandfather.find("div", class_="panel-item-info")
    stats = item_info.find_all("tr")
    for tr in stats:
        td_list = []
        for td in tr.find_all("td"):
            text = td.text
            td_list.append(text)
        weapon_stats[td_list[0]] = td_list[1]  # [0] category, td_list[1] stat
    wep_link = await get_weapon_link(name_formatted)
    weapon_stats["wepUrl"] = "https://db.fortnitetracker.com" + wep_link
    weapon_stats["imgUrl"] = "https://db.fortnitetracker.com" + img.get('src')
    return weapon_stats


async def get_weapon_stats(weapon_name):
    """ Gets actual weapon stats from the DB if it exists,
    if not creates a new record. """
    frmtd_wep = await convert_to_storable_name(weapon_name)
    wep_links = await get_all_weapon_links()
    if frmtd_wep in wep_links.keys():
        if weapondata.lookup_data(frmtd_wep) is not None:
            return weapondata.lookup_data(frmtd_wep)
        else:
            weapon_stats = await scrape_for_weapon(weapon_name)
            print(f"[{methods.get_today_date()}] "
                  f"Creating new record {weapon_name}")
            weapondata.input_data(frmtd_wep, weapon_stats["Damage"],
                                  weapon_stats["Critical Hit Chance"],
                                  weapon_stats["Critical Hit Damage"],
                                  weapon_stats["Fire Rate"],
                                  weapon_stats["Magazine Size"],
                                  weapon_stats["Range"],
                                  weapon_stats["Durability"],
                                  weapon_stats["Reload Time"],
                                  weapon_stats["Ammo Cost"],
                                  weapon_stats["Impact"],
                                  weapon_stats["wepUrl"],
                                  weapon_stats["imgUrl"])
            return weapondata.lookup_data(frmtd_wep)
    else:
        return None


async def embed_weapon_stats(ctx, arguments):
    """ Creates an embed for weapon stats """
    weapon = await get_weapon_stats(arguments)
    if weapon is None:
        print("ERROR: " + weapon)
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
        author = ctx.author.display_name
        time = methods.get_time()
        weapon_gathered_date = weapon["Date"]
        embed_description = (f"Statistics gathered on {weapon_gathered_date}\n"
                             f"For more information, click the link above.")
        embed = Embed(title=wep_name, url=wep_url,
                      description=embed_description, color=embed_colour)
        embed.set_author(name="Weapon Lookup", icon_url=thumbnail)
        embed_general_value = (f"Fire Rate: {fire_rate}\n"
                               f"Duability: {durability}\n")
        embed.add_field(name="General", value=embed_general_value)
        embed_damage_value = (f"Damage: {damage}\n"
                              f"Impact: {impact}\n"
                              f"Range: {range}\n"
                              f"Critical Damage: {crit_dmg}\n"
                              f"Critical Damage Chance: {crit_chance}")
        embed.add_field(name="Damage", value=embed_damage_value)
        embed_magazine_value = (f"Size: {mag_size}\n"
                                f"Ammo Cost: {ammo_cost}\n"
                                f"Reload Time: {reload_time}")
        embed.add_field(name="Magazine", value=embed_magazine_value)
        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=f"Generated by @{author}, {time}")
        await ctx.send(embed=embed)


async def embed_related_searches(ctx, arguments):
    weapon_links = await get_all_weapon_links()
    related_searches = difflib.get_close_matches(arguments,
                                                 weapon_links.keys(), 4, 0.4)
    formatted_searches = []
    if not related_searches:
        related_description = "\n*weapon name rarity*"
    else:
        for search in related_searches:
            search = search.replace("-", " ").title()
            formatted_searches.append(search)
        formatted_str = "\n".join(formatted_searches)
        related_description = f"""
*{formatted_str}*
       """
    embed = Embed(title="We couldn't find that weapon.",
                  description=related_description,
                  color=0xff8000)
    await ctx.send(embed=embed)


async def handle_command(ctx, arguments):
    """ Handles the !lookup weapon and relate searches """
    stats = await get_weapon_stats(arguments)
    if stats is None:
        await embed_related_searches(ctx, arguments)
    else:
        await embed_weapon_stats(ctx, arguments)
