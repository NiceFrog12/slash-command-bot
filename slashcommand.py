import discord
from discord.ext import commands
import random
import requests
import asyncio
from functions import foxpic

# Initialize the bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Provide the guild IDs where the slash command will appear
GUILD_IDS = []  # Replace with your actual guild IDs

@bot.event
async def on_ready():
    print(f'I am in! My codename is: "{bot.user}"')

    
@bot.event  
async def on_message(message): 
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return 
    # Convert the message to lowercase for case-insensitive comparison
    msg = message.content.lower()
    if message.author.id == 1133649297288728606:
        if '32' in message.content or "3 2" in message.content:
            try:
                await message.delete()
            except discord.errors.Forbidden:
                print("oopsie doopsey, there seems to be a fucky wucky :3")
            except discord.errors.HTTPException as e:
                print(f"oopsie doopsey, there seems to be a fucky wucky :3 {e}")
    # Check if the message is 'test' and respond
    elif msg == 'test':
        await message.channel.send("no")

    elif "да" in msg:
        await message.channel.send("test")

    elif "xd" in msg:
        await message.channel.send("real")

    elif "hi" in msg or "hai" in msg or "hello" in msg or "sup" in msg or "hey" in msg:
        await message.channel.send("helo xd")
    elif "niceguy" in msg:
        await message.channel.send("leave him alone :sob:")
    #Важно для работы команд!! 
    await bot.process_commands(message)    


@bot.slash_command(
  name="random_choice",
  description="chooses a random thing off the list you provide",
  guild_ids=GUILD_IDS
)
async def choose(ctx: discord.ApplicationContext, 
                 choices: discord.Option(str, "Choices (comma-separated)", required=True)):
    """Chooses between multiple choices."""
    choice_list = choices.split(',')
    await ctx.respond(random.choice(choice_list))#, ephemeral = True)

#spam
@bot.slash_command(
        name="repeat",
        description='Repeats your message up to 30 times (only you can see it)',
        guild_ids=GUILD_IDS
)
@commands.cooldown(1, 30, commands.BucketType.user)
async def repeat(ctx, times: int, content='repeating...'):
    for i in range(times):
        await ctx.respond(content, ephemeral=True)
#error for the command above
@repeat.error
async def repeat_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = round(error.retry_after)
        await ctx.respond(f"stop spamming mf. wait like {remaining_time} seconds")#, ephemeral = True)           note for self: you can delete the # to make it ephemeral, aka only show to the person activating the command

#generator of passwords
@bot.slash_command(
        name="generator",
        description="Generates a random string with however many symbols you want (only you will see it)",
        guild_ids=GUILD_IDS
)
async def gen(ctx, length: int):
    generated = ''
    for i in range(length):
        Symbols = "+-_/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        randomised = random.choice(Symbols)
        generated += randomised

    await ctx.respond(generated, ephemeral = True)


@bot.slash_command(
        name="dictionary",
        description="searches up the meaning of a word out of urban dictionary",
        guild_ids=GUILD_IDS
)
async def urban_dictionary(ctx, term):
    url = f"https://api.urbandictionary.com/v0/define?term={term}"
    response = requests.get(url)
    data = response.json()
    if 'list' in data:
        if data['list']:
            top_definition = data['list'][0]['definition']
            example = data['list'][0]['example']
            await ctx.respond(f"**Definition:** {top_definition}\n**Example:** {example}")#, ephemeral=True)  note for self: you can delete the # to make it ephemeral, aka only show to the person activating the command
        else:
            await ctx.respond("No definition found.", ephemeral=True)
    else:
        await ctx.respond("Error retrieving definition.", ephemeral=True)

@bot.slash_command(
        name = "bait",
        description = "bait or mental retardation?",
        guild_ids = GUILD_IDS
)
async def bait(ctx):
    await ctx.respond("bait or mental retardation?")
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    options = ["bait", "mental"]
    try:
        response = await bot.wait_for('message', check=check, timeout=10)  # Wait for user response
        choice = response.content.lower()
        #bait
        if choice == "bait":
            await ctx.respond("Look, this bloke took the bait, laugh at him everyone :joy: :joy: :joy: :skull: :skull: :skull:")
        #MR
        elif choice == "mental":
            await ctx.respond("my boy is mental")
            
            #error
        else:
            await ctx.respond("Learn how to type bro (u prob made a typo)")
    except asyncio.TimeoutError:
        await ctx.respond("Slow ass")

@bot.slash_command(
        name = "fox",
        description = "sends a random picture of a fox",
        guild_ids = GUILD_IDS)
        
async def fox(ctx: discord.ApplicationContext,
              amount: discord.Option(int, "How many pictures do you wish to see? 1-5", required=True)):
    if amount <= 5:
        image_urls = [foxpic() for picture in range(amount)]
        for picture in image_urls:
            await ctx.respond(picture)
    else:
        await ctx.respond("You can only get 1-5 pictures.")

@bot.slash_command(
        name="help",
        description="Get a list of all commands",
        guild_ids=GUILD_IDS
)
async def help_command(ctx: discord.ApplicationContext):
    embed = discord.Embed(title="Help", description="List of all commands", color=discord.Color.blue())
    commands_list = [
        {"name": "/random_choice [choices]", "description": "Chooses a random thing off the list you provide (comma-separated)."},
        {"name": "/repeat [times] [content]", "description": "Repeats your message up to 30 times. (only you see it)"},
        {"name": "/generator [length]", "description": "Generates a random string with however many symbols you want. (only you will see it)"},
        {"name": "/dictionary [term]", "description": "Searches up the meaning of a word from Urban Dictionary."},
        {"name": "/bait", "description": "Bait or mental retardation?"},
        {"name": "/fox [amount]", "description": "Sends a random picture of a fox (1-5)."}
    ]

    for command in commands_list:
        embed.add_field(name=command["name"], value=command["description"], inline=False)

    await ctx.respond(embed=embed)


#change the token if you need to
token = "put your own one in here"
bot.run(token)
