import sqlite3
from .methods import get_today_date

conn = sqlite3.connect('data/weapons.db')
cur = conn.cursor()


def create_table():
    """ Creates weapons table in the database """
    cur.execute('''CREATE TABLE IF NOT EXISTS weapons(datestamp TEXT,
                weapon TEXT, damage INTEGER, critChance TEXT,
                critDamage TEXT, fireRate INTEGER, magSize INTEGER,
                wepRange INTEGER, wepDurability TEXT, reloadTime TEXT,
                ammoCost INTEGER, impact INTEGER, wepUrl TEXT, imgUrl TEXT)''')


def input_data(weapon_name, damage, crit_chance, crit_damage, fire_rate,
               mag_size, wep_range, wep_durability, reload_time,
               ammo_cost, impact, wep_url, img_url):
    """ Inputs data into the weapons table """
    today = get_today_date()
    create_table()
    cur.execute("""INSERT INTO weapons (datestamp, weapon, damage, critChance,
                critDamage, fireRate, magSize, wepRange, wepDurability,
                reloadTime, ammoCost, impact, wepUrl, imgUrl)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (today, weapon_name, damage, crit_chance, crit_damage,
                 fire_rate, mag_size, wep_range, wep_durability, reload_time,
                 ammo_cost, impact, wep_url, img_url))
    conn.commit()


def lookup_data(weapon_name):
    """ Queries for a certain weapon name in format weapon-name-rarity """
    create_table()
    cur.execute("SELECT * FROM weapons WHERE weapon = ?;", (weapon_name,))
    formatted_weapon_name = weapon_name.replace("-", " ")
    formatted_weapon_name = formatted_weapon_name.title()
    all_rows = cur.fetchall()
    if len(all_rows) > 0:
        weapon_dict = {}
        for row in all_rows:
            weapon_dict = {
                "Name": formatted_weapon_name,
                "Rarity": weapon_name.split("-")[-1],
                "Date": row[0],
                "Weapon": row[1],
                "Damage": row[2],
                "Critical Hit Chance": row[3],
                "Critical Damage": row[4],
                "Fire Rate": row[5],
                "Magazine Size": row[6],
                "Range": row[7],
                "Durability": row[8],
                "Reload Time": row[9],
                "Ammo Cost": row[10],
                "Impact": row[11],
                "wepUrl": row[12],
                "imgUrl": row[13]
            }
        return weapon_dict
    else:
        return None
