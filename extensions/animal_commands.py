import discord, aiohttp, extensions.cataas_constants
from discord.ext import commands
from dataclasses import dataclass

@dataclass
class Cat:
    tags: list
    url: str = ''

@commands.hybrid_command(name="catpls")
async def catpls(ctx, tag: str = None):
    async with aiohttp.ClientSession() as session:
        base_url = extensions.cataas_constants.CATAAS_BASE_URL
        json_attribute = extensions.cataas_constants.JSON_ATTRIBUTE

        if tag == None:
            url = base_url + f"/cat{json_attribute}"
        else:
            url = base_url + f"/cat/{tag}{json_attribute}"

        async with session.get(url) as response:
            if response.status != 200:
                await ctx.send("we couldn't find a cat with that tag :(")
                return

            response = await response.json()
            cat_response = Cat([])
            cat_response.url = base_url + response['url']
            cat_response.tags = [tag for tag in response['tags']]

            embed = discord.Embed(color=0xFF5733)
            embed.set_footer(text = ', '.join([tag for tag in cat_response.tags]))
            embed.set_author(name=cat_response.url)
            if 'gif' in cat_response.tags:
                print(f"downloading {cat_response.url} to display as a .gif")
                # TODO: download the image to display as a .gif
            embed.set_image(url=cat_response.url)
            await ctx.send(embed=embed)

async def setup(bot):
    bot.add_command(catpls)
