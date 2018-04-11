import datetime
import json

# Config stuff
def config_load():
    """ Loads the config from data/ """
    with open('data/config.json', 'r', encoding='utf-8') as doc:
        #  Please make sure encoding is correct, especially after editing the config file
        return json.load(doc)

#Date/Time stuff
def get_today_date():
    today = datetime.datetime.now()
    formatted_today = today.strftime('%d-%b-%Y %H:%M:%S')
    return formatted_today
