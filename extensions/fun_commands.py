import discord
from discord.ext import commands

@commands.hybrid_command(name="blarg", description="Blarg")
async def blarg(ctx):
    await ctx.send(f"Blarg!")

@commands.hybrid_command(name="hello", description="Says hello!")
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.display_name} 👋")

async def setup(bot):
    bot.add_command(blarg)
    bot.add_command(hello)
