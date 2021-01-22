
# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from sys import argv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot=commands.Bot(command_prefix='~')
bot.remove_command('help')

def is_dm():
	def predicate(ctx):
		return ctx.guild == None
	return commands.check(predicate)

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game('Guarding Feedback'))
	print(f'{bot.user.name}is up')

#this is incase anyone wants the submissions to be via dm's, tho i gave up early on it. finish it yoself
#@bot.command(name='priv_feedback')
#async def priv_feedback(ctx):
#	member=ctx.author
#	await member.create_dm()
#	await member.dm_channel.send(f"sup {member.name}, let's get you set up")
#	await member.dm_channel.send(f"send your info in this format: ~submit [Songname] [description IN PERENTHESIS] [link to your song]")
#	await ctx.send('check your dms ;)')

@bot.event
async def on_guild_join(guild):
	channel = bot.get_channel(700553690200670248)
	await channel.send("Well, well, well. Looks like theres a new sheriff in town. Ya'll couldn't stay in line and gave the mods a hard time. So now I'm here to clean up feedback chat and I'm here to stay\n>.>\n<.<")

@bot.command(name='help')
async def help(ctx, arg1=""):
	human=ctx.author
	suffix=str(arg1)
	await ctx.message.delete()
	await human.create_dm()
	if suffix == "":
		await human.dm_channel.send(f"hey there {human.mention} :wave:. Heres how I work \n```command list:~feedback, ~submit \nyou can type ~help [command name] for info on how to use it\nyou can not submit a song unless you have given feedback first\n \nfor any specific inquiries about the bots functionality, code, or support feel free to hmu @creepzer#3030 ```")
	elif suffix == 'submit' or suffix == '~submit':
		await human.dm_channel.send(f"`~submit [1-3] [a link to your song]`\n 1 = song is a Work in Progress\n2 = Song is a Rough Draft\n3 = Song is a Finished Product")
	elif suffix == 'feedback' or suffix == '~feedback':
		await human.dm_channel.send(f"`~feedback [@ the person you are giving feedback to] [your feedback content goes here]`\n Your feedback has to be more then 200 characters so put some thought into it")

@bot.command(name='submit')
@commands.has_role('feedback warrior')
async def submit(ctx,a: int, *, content):
#spicy modular values because y not
	channel = bot.get_channel(700553690200670248)
	role=get(ctx.author.guild.roles, name='feedback warrior')
	message=ctx.message
	member=ctx.author
	link=str(content)
	progress=a
	await message.delete()

#a lazy way of setting values to numbers cuz..... yea
	if progress == 1:
		prog="Work in Progress"
	elif progress == 2:
		prog="Rough Draft"
	elif progress == 3:
		prog="Finished Song"
	else:
		await channel.send("Please enter a valid number, it's 1-3")
#this keeps ppl from uploading files and such. becausse vulnerabilites on the server yaddayadda
	if len(message.attachments) > 0:
		await channel.send(f"Your submission has to be a link {ctx.author.mention}!")
		return
#the if statement just makes sure the 1st parameter is in the range accepted and isn't used as an overflow vuln
	if progress<=3 and progress>=1:
		await member.remove_roles(role)
		await channel.send(f"artist:{ctx.author.mention} \nThis song is a {prog} \n{link}")


@bot.event
async def on_command_error(ctx, error):
	channel = bot.get_channel(700553690200670248)
	message=ctx.message
	if message.channel.type == "dm" and (str(message) == "~feedback" or str(message) == "~submit"):
		await ctx.send("you can't run the commands from dm's. Go to the feedback channel")
		return
#this one is a cool trick. basuically once you give a feedback that goes through, you get a role
#and you can only submit your song for feedback if you have that role
	if isinstance(error, commands.errors.MissingRole):
		await channel.send(f'**you have to give feedback before you can submit** {ctx.message.author.mention} **>:c**')
		await message.delete()
		return
#if people don't fillout the command correctly it tells them to try again and points instructions
	if isinstance(error, commands.errors.MissingRequiredArgument):
		await message.delete()
		await channel.send(f"Let's try that again {ctx.author.mention} but make sure everything is there, try ~help if you are stuck ^-^")
		return
	if isinstance(error, commands.errors.CheckFailure):
		await ctx.send("Sorry you can't run commands from dm's. Go to the feedback channel for that ")
		return
	await bot.process_commands(message)

@bot.command(name='feedback')
async def feedback(ctx, arg1, *, content):
#just a bunch of values being stored to make the method more modular later on "totally not beacuse i'm lazy"
	role=get(ctx.author.guild.roles, name='feedback role')
	channel = bot.get_channel(700553690200670248)
	message=ctx.message
	number=len(str(content))
	userMention=str(arg1)
	cawntent=str(content)
	UserCheck=ctx.author.id
	if ctx.message.guild == None:
		await ctx.send("Sorry you can't run commands from dm's. Go to the feedback channel for that")
		return
	else:
		await message.delete()
#ensures that they are @'ing a person with the feedback so the bot mentions them in the reprint
		if "@" not in userMention:
			await channel.send(f"Yo {ctx.author.mention} you gotta @ the person you are giving feedback to")
			return
#to ensure ppl can't abuse feedback and give feedback to themselves
		if ("<@{UserCheck}>") == userMention or (f"<@!{UserCheck}>") ==userMention:
			await channel.send(f'Nice try {ctx.author.mention}, but give feedback to someone *OTHER then yourself*')
			return
#makes sure the feedback is over 169 characters, I would've put 200 but 169 is funnier and more lenniant to the users
		if number<169:
			await channel.send(f'you can give better feedback then that {ctx.author.mention}, sweeten it up to 200+characters')
		elif number>=169:
			if '[' in cawntent or ']' in cawntent:
				cawntent = cawntent.replace("[","(")
				cawntent = cawntent.replace("]", ")")
			await channel.send(f"{ctx.message.author.mention} gave feedback to {userMention} ```ini\n[{cawntent}]```")
			await ctx.author.add_roles(role)
@bot.event
async def on_message(message):
#ensures the bot doesn't delete it's own messages lol
	if message.author == bot.user:
		return
	if message.guild == None:
		pass
	else:
#locks the cammand to a channel called 'feedback'
		if message.channel.name=='feedback':

			stuff=message.content
		if len(message.attachments) > 0 and message.channel.name =='feedback':
			await message.channel.purge(limit=1)
			await message.channel.send(f"No files in this chat please {message.author.mention}")
#deletes messages with links unless they are part of a command
		if 'http' in stuff:
			if "~submit" in stuff or "~feedback" in stuff:
				await bot.process_commands(message)
			else:
				await message.channel.purge(limit=1)
				await message.channel.send(f'{message.author.mention} only links for submissions or feedback examples O.O')
	await bot.process_commands(message)


bot.run(TOKEN)
