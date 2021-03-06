import discord, asyncio, sys, time, os
from discord.ext import commands

import gamedb, strings, users

#bot.get_channel('312676555514183681')

bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'))

@bot.event
async def on_ready():
    users.loadAllCharacters()

    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    print(message.author.id, message.channel)

    await bot.process_commands(message)

@bot.command(pass_context=True)
async def join(ctx, name: str = None):

    if name == None:
        await bot.say(strings.all["join"]["no_arg"])
    else:
        player_id = ctx.message.author.id
        result = users.addNewCharacter(player_id, name)

        if result is None:
            await bot.say(strings.all["join"]["taken"])
        elif result is False:
            await bot.say(strings.all["join"]["exists"])
        else:
            await bot.say(strings.all["join"]["added"].format(name))
            await bot.send_message(ctx.message.author, "what up")

@bot.command(pass_context=True)
async def name(ctx, name: str = None):

    if name == None:
        await bot.say(strings.all["name"]["no_arg"])
    else:
        result = users.setCharacterName(ctx.message.author.id, name)

        if result is None:
            await bot.say(strings.all["name"]["notfound"])
        elif result is False:
            await bot.say(strings.all["name"]["taken"])
        else:
            await bot.say((strings.all["name"]["updated"]).format(name))

@bot.command(pass_context=True)
async def stats(ctx):
    result = users.getCharacterById(ctx.message.author.id)

    # Did not have a character matching id.
    if result == None:
        await bot.say(strings.all["stats"]["notfound"])
    else:
        vals = result.getValues()

        msg = strings.all["stats"]["all_stats"]

        # Include a message stating that there are unspent ability points (or not).
        if vals[3] > 0:
            msg += strings.all["stats"]["unspent"]

        await bot.say(msg.format(*vals))

@bot.command()
async def whois(name: str = None):

    if name == None:
        await bot.say(strings.all["whois"]["no_arg"])
    else:
        result = gamedb.whois(name)

        if result == None:
            await bot.say(strings.all["whois"]["notfound"].format(name))
        else:
            user_id = result[0]
            display_name = None

            # Check all members in all servers (should just be one)
            for server in bot.servers:
                for member in server.members:
                    if member.id == user_id:
                        display_name = member.display_name

            if display_name == None:
                await bot.say(strings.all["whois"]["notfound"].format(name))
            else:
                await bot.say(strings.all["whois"]["found"].format(name, display_name))

@bot.command()
async def players():
    pass
    #all_players = gamedb.get_all_characters()

    #msg = strings.all["players"]["list"]
    #for player, level in all_players:
    #    msg += strings.all["players"]["template"].format(player, level)

    #await bot.say(msg)

@bot.command()
async def save():
    users.saveAllCharacters()

@bot.command(pass_context=True)
async def stop(ctx):
    if ctx.message.author.id == sys.argv[2]:
        users.saveAllCharacters()
        os._exit(0)

bot.run(sys.argv[1])
