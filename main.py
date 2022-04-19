import discord
import os
from discord.ext import commands
from webserver import keep_alive
from time import sleep
intents = discord.Intents().all()
intents.members = True
bot = commands.Bot(command_prefix="]", intents=intents, activity = discord.Streaming(name="your mom", url="https://twitch.tv/Bawkworm"), description="Made with lots of sleep deprivation!", case_insensitive=True)
ping = []
people = ""
pingmsg = "This week these people asked to play MC: \n"
points = {}
send = True
buddy = False

@bot.event
async def on_connect():
  print("connected")

@bot.event
async def on_member_join(member):
  points[str(member.id)] = 0

@bot.command(name="buddy-on", description="Buddy on")
async def toggleON(ctx):
  global buddy
  buddy = True
  await ctx.send("Toggled on!")

@bot.command(name="buddy-off", description="Buddy off")
async def toggleOFF(ctx: commands.Context):
  global buddy
  buddy = False
  await ctx.send("Toggled off!")

@bot.event
async def on_message(message):
  lineloc = []
  send = True
  cont = message.content
  x = cont.lower()
  msg = x.split(' ')
  if '\n' in list(x):
    msg.clear()
    msg = list(x)
    for i in range(len(list(x))):
      if list(x)[i] == '\n':
        lineloc.append(i)
    msg = ''.join(msg)
    for loc in lineloc:
      msg = msg[:loc] + '-' + msg[loc:]
    msg = msg.split(' ')

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
  if ']add' in x:
    ping.append(f"@{x[5:]} \n")
    await message.channel.send("Added!")
  if ']del' in x:
    ping.pop(int(x[5:]) - 1)
    await message.channel.send("Deleted!")
  if points[message.author.id] > 2:
    ping.append(f'<@{message.author.id}>: "{x}" \n')
    if ping.count(f'<@{message.author.id}>: "{x}" \n') > 1:
      for i in range(ping.count(f'<@{message.author.id}>: "{x}" \n') - 1):
        ping.remove(f'<@{message.author.id}>: "{x}"')
    if send == True and buddy == True:  
      await message.channel.send("For friends I'd suggest looking in <#864405889490485248>, for realms/servers to play on I suggest you look in <#864423583236227102> Alternatively, we have an smp you could join with about a weeks wait time, for more info on that read <#853336509419749376> We are also partnered with a awesome discord server called Minecraft: Supernova that is host to multiple amazing minigames and realms, for more info on that you can check <#917508508579160064>")
  if message.content == ']smp-apply':
    questions = ['What is your chat level? (you need at least chat level 7)', 'What is your gamertag?', 'Did you participate in any server events? (participating lowers chat level requirement to 3)']
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
      await anschan.send(f"<@{message.author.id}>'s SMP application! \n {' '.join(application)}")

@bot.command(name="buddy", description="Pings everyone who asks to play")
async def ping_week(ctx: commands.Context):
  people = ' '.join(ping)
  await ctx.send(pingmsg + people)

@bot.command(name="clear", description="Clears the ping list")
async def clear(ctx: commands.Context):
  ping.clear()
  await ctx.send("Cleared!")

# @bot.command(name="ping")
# async def pingy(ctx):
#     await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


# @bot.command(name="changelognotes")
# async def cnotes(message, args):
#   await message.channel.send(f'{message.author} : {args} , <t:{message.id}>')
  

keep_alive()
bot.run(os.getenv("token"))