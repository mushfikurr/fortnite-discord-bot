# Raptor
Your Discord companion for everything Fortnite.  


## Getting started  
Using Raptor running on your machine requires `Python` and `Pipenv`. It will also require the generation of a Discord bot token, and a Fortnite Tracker API token. 

### Prerequisities  
Install [Python](https://www.python.org/), to run .py files.  
Install Pipenv, to handle the virtual environment: `pip install pipenv`    
For more information on installing pipenv, refer [here](https://docs.pipenv.org/).  

### Installing dependencies
Clone this repository to a folder. This will be the directory that the bots will run in.  
Direct your command-line (bash/cmd/etc) to this directory.  
Run `pipenv sync --dev`, this will install all packages specified in `Pipfile.lock`, which should only be `Discord.py (rewrite)` unless changed in the future.  
Once this is done, you have all dependencies.  


## Setting up the bot
Now that you have installed dependencies to run the bot, you can setup the bot. This will ensure the bot runs smoothly.

### Directories and configs
Create a directory called `data` inside the bots directory. Inside here create another file called `config.json`.  
This file **MUST INCLUDE** a `description`, `token`, and `trn-token`, or the bot will fail to run.  
```
{
    "description": "Hi! I'm a sample description",
    "token": "XXXXXXXXXXXXXXXX",
    "trn-token": "YYYYYYYYY"
}
```
`token` is where your the discord token goes.  
`trn-token` is where your Fortnite Tracker API token goes.  
This file can easily be expanded, if you wanted to add more features which requires a config.

### Generating tokens
Generating a discord token is explained [here](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token). Once you get the token, place it in the config.json file instead of the source.  
Generating a Fortnite Tracker API token is simple, it can be requested [here](https://fortnitetracker.com/site-api)


## Deploying the bot
You can now deploy the bot after all dependencies, directories and tokens are created.  
`py main.py` will run the main .py file - which handles the bot. This command may vary across different operating systems.


## Features
Features of the RAPTOR bot.

### Statistics
You can easily pull statistics from the Fortnite Tracker API.  
`!stats` shows all commands available for the command group stats. 

### Lookup
Looks up for any item in Fortnite, returning relevant statistics and rarities.  
`!lookup` shows all commands available for the command group lookup.

### Patch
Returns the latest patch notes for Fortnite.   
`!patch` shows all commands available for the command group patch.

### Status
Returns the status of the fortnite servers.  
`!status` shows all commands available for the command group status.








