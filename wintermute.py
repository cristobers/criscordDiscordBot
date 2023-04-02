#!/usr/bin/python3

import discord, asyncio, random, io, aiohttp, getCatGifs
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timedelta
# from discord.ext.commands import CommandNotFound, app_commands
from discord.utils import get
from json import load
from list import dogList

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="/", intents=intents)

with open("clientkey.json") as f:
    data = load(f)
    token = data["TOKEN"]

@tasks.loop(minutes=30)
async def stinkyGamePlayerRemover(bot):
    gamesThatSmell = ['league of legends', 'valorant']
    channel, guild = bot.get_channel(823948479331041312), bot.get_guild(823948478786306049)

    for member in guild.members:
        for activity in member.activities:
            if activity.type == discord.ActivityType.playing:
                if activity.name.lower() in gamesThatSmell:
                    print(f"{member.name} was found playing {member.activity.name}")
                    await channel.send(f":O {member.mention} i have detected that you are playing a stinky game, is this true??? :(")

            if isinstance(activity, discord.Spotify):
                if 'Weezer' == activity.artist:
                    await channel.send(f"WEEZOID DETECTED {member.mention} banishment!!!")
                    print(member, activity.artist)
                    if not member.is_timed_out():
                        now = datetime.now()
                        await member.timeout(discord.utils.utcnow() + timedelta(minutes = 30))


@bot.tree.command(name="catpls")
async def cat(interaction: discord.Interaction, tag: str = None):
    async with aiohttp.ClientSession() as session:
        url = "https://cataas.com"
        jsonAttribute = "?json=true"
        baseurl = url

        if tag != None:
            url = url + f"/cat/{tag}{jsonAttribute}" 
        else:
            url = url + f"/cat{jsonAttribute}" 

        async with session.get(url) as a:
            # if i'm downloading something, the bot suffers and cats cannot load fast enough !!!
            if a.status != 200:
                await interaction.response.send_message("we couldn't find a cat with that tag :(")
                return

            a = await a.json()
            catTags = 'tags: ' + ' '.join([tag for tag in a['tags']])

            embed = discord.Embed(color=0xFF5733)
            embed.set_footer(text=catTags)
            catImage = f"{baseurl}{a['url']}"               

            if 'gif' in catTags:
                catGIFBytes = await getCatGifs.main(catImage)         
                embed.set_author(name=f"{catImage}")
                discordCatGIFAttachment = discord.File(catGIFBytes, filename="cat.gif")
                embed.set_image(url="attachment://{cat.gif}")
                try:
                    await interaction.response.send_message(file=discordCatGIFAttachment, embed=embed)
                except discord.errors.HttpException as e:
                    await interaction.response.send_message(f"Cannot send GIF, HTTP error {e.status} {e.text}.")
            else:
                embed.set_author(name=f"{catImage}")
                embed.set_image(url=catImage)
                await interaction.response.send_message(embed=embed)

async def dog_autocompletion(
    interaction: discord.Interaction,
    current: str
) -> list[app_commands.Choice[str]]:
    data = []
    for dog_choice in dogList:
        if current.lower() in dog_choice.lower():
            data.append(app_commands.Choice(name=dog_choice, value=dog_choice))
    if len(data) > 25:
        del data[25:]
    return data

@bot.tree.command(name="dogpls")
@app_commands.autocomplete(breed=dog_autocompletion)
async def dog(interaction: discord.Interaction, breed: str = None):
    async with aiohttp.ClientSession() as session: 
        dogURL = "https://dog.ceo/api/"
        if breed != None:
            if '-' in breed:
                breeds = breed.replace('-', '/')
                dogURL = f"{dogURL}breed/{breeds}/images/random/"
                print(dogURL)
            else:
                dogURL = f"{dogURL}breed/{breed}/images/random/"
        else:
            dogURL = f"{dogURL}breeds/image/random/" 
        try:
            async with session.get(dogURL) as response:
                if response.status != 200:
                    await interaction.response.send_message("We couldn't seem to find a dog for you D:")
                    return
                response = await response.json()
                dogTags = response["message"]
                embed = discord.Embed(color=0xFF5733)
                embed.set_author(name=str(dogTags))
                embed.set_image(url=dogTags)
                await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(f"An error has occured: {e}")

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    await stinkyGamePlayerRemover.start(bot)
bot.run(token)
