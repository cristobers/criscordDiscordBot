#!/usr/bin/python3

import discord, asyncio, random, io, aiohttp
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timedelta
from discord.utils import get
from json import load

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="/", intents=intents)

with open("clientkey.json") as f:
    data = load(f)
    token = data["TOKEN"]

@bot.event
async def on_ready():
    test = discord.abc.Snowflake
    test.id = 823948478786306049

    await bot.load_extension("extensions.animal_commands")
    await bot.load_extension("extensions.fun_commands")

    synced = await bot.tree.sync(guild=test)
    print(f"Synced {len(synced)} commands")
    print("Bot is up")
bot.run(token)
