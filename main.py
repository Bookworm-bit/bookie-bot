import discord
import os
from discord.ext import commands
from webserver import keep_alive
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option 
import time
from discord.ui import Button, View
intents = discord.Intents().all()
intents.members = True
bot = commands.Bot(command_prefix="]", intents=intents, activity = discord.Streaming(name="your mom", url="https://twitch.tv/Bawkworm"), description="Made with lots of sleep deprivation!", case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True)
ping = []
people = ""
pingmsg = "This week these people asked to play MC: \n"
points = {}
# pingtag = {}
# pingtagevent = False
# pingtagpart = []
send = True
changelog = []
buddy = False

@bot.event
async def on_connect():
  print("connected")

@bot.event
async def on_member_join(member):
  points[str(member.id)] = 0

@bot.command(name="buddy-on", description="Buddy on")
@commands.has_role("^^^——————{Mod Team}——————^^^")
async def toggleON(ctx):
  global buddy
  buddy = True
  await ctx.send("Toggled on!")

@bot.command(name="buddy-off", description="Buddy off")
@commands.has_role("^^^——————{Mod Team}——————^^^")
async def toggleOFF(ctx: commands.Context):
  global buddy
  buddy = False
  await ctx.send("Toggled off!")

@bot.event
async def on_message(message):
  print(f'#{message.channel} - @{message.author} ({message.author.id}): {message.content}')
  msg = []
  send = True
  cont = message.content
  x = cont.lower()
  lb = list(x)
  if '\n' in lb:
    for i in range(len(lb) - lb.count('\n')):
      if lb[i] == '\n':
        lb.pop(i)
        lb.insert(i, ' ')
    msg = ''.join(lb).split(" ")
  else:
    msg = x.split(' ')

  # if pingtagevent == True:
  #   if message.author.id in pingtagpart and message.mentions[0].id in pingtagpart and 'ping' in message:
  #     pinged = message.mentions[0].id
  #     while True:
  #       pingtag[pinged] += 1
  #       msg = await bot.wait_for('message')
  #       if msg.author.id == pinged and msg.mentions[0] != None and 'ping' in message:
  #         break
  #       time.sleep(1)
  
  await bot.process_commands(message)
  guild = bot.get_guild(738532090865254422)
  for member in guild.members:
    points[member.id] = 0
  for item in points:
    points[item] = 0
  if message.author == bot.user:
    return
  if message.author.bot:
    return
  if message.channel.id == 864423583236227102:
    return
    send = False
  value1 = ['who', 'wanna', 'want to', 'dm', 'pm']
  value2 = ['bedrock', 'anyone', 'interest', 'world', 'realm']
  value3 = ['eggwars', 'skywars', 'skyblock', 'minecraft', 'mc']
  value4 = ['play', 'hive', 'cubecraft', 'survival']
  smp = ['join', 'how', 'smp', 'realm', 'server', 'do']
  smpcount = 0

  for item in msg:
    if item in value1:
      points[message.author.id] += 0.5
    if item in value2:
      points[message.author.id] += 1
    if item in value3:
      points[message.author.id] += 1.5
    if item in value4:
      points[message.author.id] += 2

  for thing in msg:
    if thing in smp:
      smpcount += 1
  if smpcount >= 3:
    await message.channel.send('To join the smp you need to first click the "s" reaction in <#853336509419749376> Next you chat for about 10 to 20 minutes so you reach chat level 7 (this can be lowered to chat level 3 if you participate in a server event). NOTE: Pinging Pollo to whitelist you before you meet the requirements is a great way to not get into the smp.')
    if points[message.author.id] > 2:
      ping.append(f'<@{message.author.id}>: "{x}" <t:{round(time.time())}> \n')
    if ping.count(f'<@{message.author.id}>: "{x}" <t:{round(time.time())}> \n') > 1:
      for i in range(ping.count(f'<@{message.author.id}>: "{x}" <t:{round(time.time())}> \n') - 1):
        ping.remove(f'<@{message.author.id}>: "{x}" <t:{round(time.time())}> \n')
      if send == True and buddy == True:  
        await message.channel.send("For friends I'd suggest looking in <#864405889490485248>, for realms/servers to play on I suggest you look in <#864423583236227102> Alternatively, we have an smp you could join with about a weeks wait time, for more info on that read <#853336509419749376> We are also partnered with a awesome discord server called Minecraft: Supernova that is host to multiple amazing minigames and realms, for more info on that you can check <#917508508579160064>")

  if message.content == ']smp-apply':
    questions = ['What is your chat level?', 'What is your gamertag?', 'Did you participate in any server events? (participating lowers chat level requirement to 3)']
    answers = []
    application = []
    applicant = message.author
    anschan = bot.get_channel(867126999770988545)
    await applicant.send("Starting your application process!")
    await message.channel.send("Started!")
    def check(m):
      if m.content is not None and isinstance(m.channel, discord.channel.DMChannel):
        return True
      else:
        return False
    for i in range(3):
      await applicant.send(questions[i])
      msg = await bot.wait_for('message', check=check)
      if applicant == message.author:
        answers.append(f'{msg.content} \n')
    await applicant.send('You have reached the end of this application! Please type "submit" to sumbit')
    msg = await bot.wait_for('message', check=check)
    if "submit" in msg.content.lower():
      await applicant.send("Submitted!")
      for i in range(3):
        application.append(f'{i+1}: `{questions[i]}` {answers[i]} \n')
      await anschan.send(f"<@{message.author.id}>'s SMP application! \n {' '.join(application)} \nRecieved at <t:{round(time.time())}>")
      applicationEmbed = discord.Embed(title=f"{message.author}'s SMP Application'", description = f"{' '.join(application)} \nRecieved at <t:{round(time.time())}>", color=discord.Colour.green())
      await message.channel.send(embed=applicationEmbed)

@bot.command(name="buddy", description="Pings everyone who asks to play")
@commands.has_role("^^^——————{Mod Team}——————^^^")
async def ping_week(ctx):
  people = ' '.join(ping)
  embeds = discord.Embed(title="This week these people asked to play Minecraft:", description=f"{people}")
  # clear = Button(label="Clear", style=discord.ButtonStyle.danger)
  # async def callback(interaction):
  #   if ctx.author == interaction.user:
  #     ping.clear()
  #     await interaction.response.send_message("Cleared!")
  #   else:
  #     await interaction.response.send_message("You do not have permission to use this button!", ephemeral=True)
  # clear.callback = callback
  # view.add_item(clear)
  await ctx.send(embed=embeds)

@bot.command(name="clear", description="Clears the ping list")
@commands.has_role("^^^——————{Mod Team}——————^^^")
async def clear(ctx: commands.Context):
  ping.clear()
  await ctx.send("Cleared!")

@bot.command(name="pong")
async def pingy(ctx):
    await ctx.send(f'Ping! {round(bot.latency * 1000)}ms')

@bot.command(name="cnotes")
@commands.has_role("^^^——————{Mod Team}——————^^^")
async def cnotes(ctx, *, args):
  channel = bot.get_channel(876552178888736789)
  await channel.send(f'{ctx.author}: \nChanged: {args} \nThis was done at <t:{int(time.time())}>')
  changelog.append(f'{ctx.author}: Changed: {args}. This was done at <t:{int(time.time())}> \n')
  print(f'{ctx.author}: Changed: {args}. This was done at <t:{int(time.time())}> \n')
  
@bot.command(name="changelogger")
@commands.has_role("^^^——————{Mod Team}——————^^^")
async def changelogger(ctx):
  channel = bot.get_channel(741419798897885304)
  await channel.send(f'This weeks changelog! \n{"".join(changelog)}. Sent at <t:{round(time.time())}>!')

# @bot.command(name="testing")
# async def testing(ctx):
#   button1 = Button(label="Testing", style=discord.ButtonStyle.danger)

#   async def callback(interaction):
#     await interaction.response.send_message("Hello")

#   button1.callback = callback
#   view = View()
#   view.add_item(button1)

#   await ctx.send("Hello", view=view)

# @bot.command(name="stopwatch")
# async def stopwatch(ctx):
#   second = 0
#   milli = 0
#   start = time.time()

#   startbutton = Button(label="Start", style=discord.ButtonStyle.green)
#   endbutton = Button(label="Stop", style=discord.ButtonStyle.danger)

#     async def callback(interaction):
#     await interaction.response.send_message("Hello")

@bot.command(name="buddy-add")
async def add(ctx, user: discord.User, *, args):
  ping.append(f'<@{user.id}>: "{args}" <t:{round(time.time())}> (Added by {ctx.author})\n')
  await ctx.send("Added!")

@bot.command(name="buddy-del")
async def delete(ctx, args):
  ping.pop(int(args) - 1)
  await ctx.send("Deleted!")

# @bot.command(name="pingtag-add")
# async def pingadd(ctx, user: discord.User):
#   pingtagpart.append(user.id)
#   await ctx.send("Added!")

# @bot.command(name="pingtag-del")
# async def pingdel(ctx, user: discord.User):
#   if user.id in pingtagpart:
#     pingtagpart.remove(user.id)
#     await ctx.send("Removed!")
#   else:
#     await ctx.send("That user was not in the list of participants!")

# @bot.command(name="pingtag-start")
# @commands.has_role("^^^——————{Mod Team}——————^^^")
# async def pingstart(ctx):
#   await ctx.send("Started!")
#   global pingtagevent
#   pingtagevent = True

# @bot.command(name="pingtag-end")
# @commands.has_role("^^^——————{Mod Team}——————^^^")
# async def pingend(ctx):
#   await ctx.send("Ended!")
#   global pingtagevent
#   pingtagevent = False


keep_alive()
bot.run(os.getenv("token"))