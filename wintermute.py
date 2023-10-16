#!/usr/bin/python3

import discord, asyncio, io 
from discord.ext import commands 
from json import load

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="/", intents=intents)
owner_id = 66183829148151808

with open("clientkey.json") as f:
    data = load(f)
    token = data["TOKEN"]

def is_owner(ctx, owner_id):
    if ctx.author.id == owner_id:
        return True
    return False

@bot.command()
async def sync(ctx):
    if is_owner(ctx, owner_id):
        synced = await bot.tree.sync()
        await ctx.send(f"Synced {len(synced)} commands")

@bot.command()
async def load(ctx, extension: str):
    if is_owner(ctx, owner_id):
        await bot.load_extension(extension)
        await ctx.send(f"Loaded {extension}")

@bot.command()
async def unload(ctx, extension: str):
    if is_owner(ctx, owner_id):
        await bot.unload_extension(extension)
        await ctx.send(f"Unloaded {extension}")

@bot.command()
async def reload(ctx, extension: str):
    if is_owner(ctx, owner_id):
        await bot.unload_extension(extension)
        await bot.load_extension(extension)
        await ctx.send(f"Reloaded {extension}")

@bot.event
async def on_ready():
    await bot.load_extension("extensions.animal_commands")
    await bot.load_extension("extensions.fun_commands")
    print("Bot is up")

bot.run(token)
