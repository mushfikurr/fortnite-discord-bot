import datetime
import json

from discord import Embed
from discord.ext import commands


def config_load():
    """ Loads the config from data/ """
    with open('data/config.json', 'r', encoding='utf-8') as doc:
        return json.load(doc)


def get_today_date():
    """ Gets the current date today in format D:M:Y H:M:S """
    today = datetime.datetime.now()
    formatted_today = today.strftime('%d-%b-%Y %H:%M:%S')
    return formatted_today


def get_time():
    """ Gets the current time in format H:M """
    today = datetime.datetime.now()
    formatted_today = today.strftime('%H:%M')
    return formatted_today


async def create_help_embed(ctx, type, error):
    """ Generates an embed with help/troubleshooting.
    Takes ctx, type (of command), and error. """
    command = ctx.command
    signature = command.signature
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):
        embed = Embed(title="Incorrect arguments",
                      description=f"!{signature}",
                      color=0xff8000)
        embed.set_footer(text="To view all commands, type !help")
    elif isinstance(error, commands.CommandInvokeError):
        if type == "Stats":
            embed = Embed(title="Could not find account",
                          description=(f"Ensure your PSN/XBL account is linked"
                                       "with Epic Games. "
                                       "For more information type !linking."),
                          color=0xff8000)
            embed.set_footer(text="To view all commands, type !help")
        elif type == "Lookup":
            embed = Embed(title="Could not find the item",
                          description=(f"Ensure the correct item "
                                       "has been entered."),
                          color=0xff8000)
            embed.set_footer(text="To view all commands, type !help")
    else:
        if type == "Stats":
            print("ERROR: " + str(error))
            embed = Embed(title="There was a problem processing your request",
                          description=f"!{signature}",
                          color=0xff8000)
            embed.add_field(name="Modes",
                            value="solo/duo/squad/lifetime",
                            inline=True)
            embed.add_field(name="Platforms",
                            value="pc/xbl/psn",
                            inline=True)
            embed.add_field(name="Username",
                            value=("You must have an Epic Account associated "
                                   "with your XBOX/PSN account. "
                                   "To find out more, type !link"),
                            inline=True)
            embed.add_field(name="Troubleshooting",
                            value=("If all arguments are correct and it is "
                                   "still not working, contact an admin."),
                            inline=True)
            embed.set_footer(text="To view all commands, type !help")
        elif type == "Lookup":
            print("ERROR: " + str(error))
            embed = Embed(title="There was a problem processing your request",
                          description=f"!{signature}",
                          color=0xff8000)
            embed.add_field(name="Weapons",
                            value=("Any weapon in Fortnite.\n"
                                   "E.g. *assault rifle burst rare*"),
                            inline=True)
            embed.add_field(name="Loot",
                            value=("Places where loot can be acquired.\n"
                                   "E.g. *chest*"),
                            inline=True)
            embed.add_field(name="Troubleshooting",
                            value=("If all arguments are correct and it is"
                                   "still not working, contact an admin."),
                            inline=True)
            embed.set_footer(text="To view all commands, type !help")
    await ctx.send(embed=embed)
