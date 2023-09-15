import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Set up the bot with command prefix '/'
bot = commands.Bot(command_prefix='/')

search_parameters = {
    "site": ["intext", "inurl", "intitle", "filetype", "ext"],
    "intext": ["site", "inurl", "intitle"],
    "inurl": ["site", "intext", "intitle"],
    "intitle": ["site", "intext", "inurl"],
    "filetype": ["site"],
    "ext": ["site"],
    "stocks": [],
    "weather": [],
    "music": [],
    "book": [],
    "movie": [],
    "phonebook": [],
    "area_code": [],
    "stock_quote": [],
    "time": [],
    "map": [],
    # Other dorks here...
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send('Sup, Dork?')

def create_google_dork(dork_type, query_parameter):
    dork_dict = {
        "site": f"site:{query_parameter}",
        "filetype": f"filetype:{query_parameter}",
        "intext": f"intext:{query_parameter}",
        "intitle": f"intitle:{query_parameter}",
        "inurl": f"inurl:{query_parameter}",
        "ext": f"ext:{query_parameter}",
        "stocks": f"stocks:{query_parameter}",
        "weather": f"weather:{query_parameter}",
        "music": f"music:{query_parameter}",
        "book": f"book:{query_parameter}",
        "movie": f"movie:{query_parameter}",
        "phonebook": f"phonebook:{query_parameter}",
        "area_code": f"area_code:{query_parameter}",
        "stock_quote": f"stock_quote:{query_parameter}",
        "time": f"time:{query_parameter}",
        "map": f"map:{query_parameter}",
    }
    return dork_dict.get(dork_type, "Invalid dork type")

@bot.command()
async def dork(ctx, dork_type, query_parameter):
    dork_query = create_google_dork(dork_type, query_parameter)
    
    # Assuming you have an API endpoint for your search engine that accepts GET requests
    response = requests.get('https://your-search-engine.com/search', params={'q': dork_query})
    
    if response.status_code == 200:
        await ctx.send(response.text)  # Modify based on your search engine's response structure
    else:
        await ctx.send(f"Error executing dork: {response.status_code}")

@bot.command()
async def build_dork(ctx):
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    await ctx.send("Step 1: Choose a starting parameter (e.g., site, intext, inurl, etc.):")
    msg = await bot.wait_for('message', check=check)
    start_param = msg.content.lower()

    if start_param in search_parameters:
        if search_parameters[start_param]:
            await ctx.send(f"Step 2: You chose {start_param}. Now choose a secondary parameter from the following options: {', '.join(search_parameters[start_param])}")
            msg = await bot.wait_for('message', check=check)
            second_param = msg.content.lower()

            if second_param in search_parameters[start_param]:
                await ctx.send(f"Building query with {start_param} and {second_param}. Now enter the value for {start_param}:")
                msg = await bot.wait_for('message', check=check)
                start_value = msg.content

                await ctx.send(f"Now enter the value for {second_param}:")
                msg = await bot.wait_for('message', check=check)
                second_value = msg.content

                query = f"{start_param}:{start_value} {second_param}:{second_value}"
                await ctx.send(f"Your search query is: {query}")
            else:
                await ctx.send("Invalid secondary parameter.")
        else:
            await ctx.send(f"Your chose a standalone parameter. Now enter the value for {start_param}:")
            msg = await bot.wait_for('message', check=check)
            start_value = msg.content

            query = f"{start_param}:{start_value}"
            await ctx.send(f"Your search query is: {query}")

    else:
        await ctx.send("Invalid starting parameter.")

# Run the bot
bot.run(TOKEN)
