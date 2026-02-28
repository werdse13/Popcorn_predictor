import discord
from discord.ext import commands
from scraper import seats_counter
import asyncio

TOKEN = "INSERT BOT TOKEN"
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def busy(ctx):
    await ctx.send("Checking today's screenings...")

    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(None, seats_counter)

    for line in results:
        await ctx.send(line)

bot.run(TOKEN)
