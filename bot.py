
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
client=discord.Client()

@bot.event
async def on_ready():
	print(f'{bot.user.name}is up')
#this is incase anyone wants the submissions to be via dm's, tho i gave up early on it. finish it yoself
#@bot.command(name='priv_feedback')
#async def priv_feedback(ctx):
#	member=ctx.author
#	await member.create_dm()
#	await member.dm_channel.send(f"sup {member.name}, let's get you set up")
#	await member.dm_channel.send(f"send your info in this format: ~submit [Songname] [description IN PERENTHESIS] [link to your song]")
#	await ctx.send('check your dms ;)')


@bot.command(name='submit')
@commands.has_role('Arole')
async def submit(ctx,a: int, *, content):
#spicy modular values because y not
	channel = bot.get_channel(800005895026901002)
	role=get(ctx.author.guild.roles, name='Arole')
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
		await channel.send("Your submission has to be a link {}!".format(ctx.author.mention))
		return
#the if statement just makes sure the 1st parameter is in the range accepted and isn't used as an overflow vuln
	if progress<=3 and progress>=1:
		await member.remove_roles(role)
		await channel.send("artist:{} \nThis song is a {} \n{}".format(member.name, prog, link))


@bot.event
async def on_command_error(ctx, error):
	channel = bot.get_channel(800005895026901002)
	message=ctx.message
#this one is a cool trick. basuically once you give a feedback that goes through, you get a role
#and you can only submit your song for feedback if you have that role
	if isinstance(error, commands.errors.CheckFailure):
		await channel.send('**you have to give feedback before you can submit** {} **>:c**'.format(ctx.message.author.mention))
		await message.delete()
#if people don't fillout the command correctly it tells them to try again and points instructions
	if isinstance(error, commands.errors.MissingRequiredArgument):
		await message.delete()
		await channel.send("Let's try that again {} but make sure everything is there, check pins for help".format(ctx.author.mention))
	await bot.process_commands(message)

@bot.command(name='feedback')
async def feedback(ctx, arg1, *, content):
#just a bunch of values being stored to make the method more modular later on "totally not beacuse i'm lazy"
	role=get(ctx.author.guild.roles, name='Arole')
	channel = bot.get_channel(800005895026901002)
	juice=ctx.message
	number=len(str(content))
	userMention=str(arg1)
	UserCheck=ctx.author.id
	await juice.delete()
#ensures that they are @'ing a person with the feedback so the bot mentions them in the reprint
	if "@" not in userMention:
		await channel.send("Yo {} you gotta @ the person you are giving feedback to".format(ctx.author.mention))
		return
#to ensure ppl can't abuse feedback and give feedback to themselves
	if ("<@{}>".format(UserCheck)) == userMention or ("<@!{}>".format(UserCheck)) ==userMention:
		await channel.send('Nice try {}, but give feedback to someone *OTHER then yourself*'.format(ctx.author.mention))
		return
#makes sure the feedback is over 169 characters, I would've put 200 but 169 is funnier and more lenniant to the users
	elif number<169:
		await channel.send('you can give better feedback then that {}, sweeten it up to 200+characters'.format(ctx.author.mention))
	elif number>=169:
		await channel.send("{} gave feedback to {}" "```ini\n[{}]```".format(ctx.message.author.mention,userMention,content))
		await ctx.author.add_roles(role)
@bot.event
async def on_message(message):
#ensures the bot doesn't delete it's own messages lol
	if message.author == bot.user:
		return
#locks the cammand to a channel called 'feedback'
	if message.channel.name=='feedback':

		stuff=message.content
	if len(message.attachments) > 0:
			await message.channel.purge(limit=1)
			await message.channel.send("No file's in this chat please {}".format(message.author.mention))
#deletes messages with links unless they are part of a command
	if 'http' in stuff:
		if "~submit" in stuff or "~feedback" in stuff:
			await bot.process_commands(message)
		else:
			await message.channel.purge(limit=1)
			await message.channel.send('only links for submissions or feedback examples O.O')
	await bot.process_commands(message)


bot.run(TOKEN)
