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

#@bot.command(name='priv_feedback')
#async def priv_feedback(ctx):
#	member=ctx.author
#	await member.create_dm()
#	await member.dm_channel.send(f"sup {member.name}, let's get you set up")
#	await member.dm_channel.send(f"send your info in this format: ~submit [Songname] [description IN PERENTHESIS] [link to your song]")
#	await ctx.send('check your dms ;)')

channel = bot.get_channel(800005895026901002)

@bot.command(name='submit')
@commands.has_role('Arole')
async def submit(ctx,a: int, *, content):
	role=get(ctx.message.server.roles, name='Arole')
	message=ctx.message
	member=ctx.author
	link=content
	progress=a
	await bot.remove_roles(member, role)
	await message.delete()
	if progress == 1:
		prog="Work in Progress"
	elif progress == 2:
		prog="Rough Draft"
	elif progress == 3:
		prog="Finished Song"
	else:
		await channel.send("Please enter a valid number, it's 1-3")
		sauce=1
	if progress<=3 and progress>=1:
		await channel.send("artist:{} \nThis song is a {} \n{}".format(member.name, prog, link))
		sauce=1


@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.CheckFailure):
		message=ctx.message
		await channel.send('**you have to give feedback before you can submit** {} **>:c**'.format(ctx.message.author.mention))
		await message.delete()
@bot.event
async def on_message(message):
	if "http" in message and not "~submit" or "~feedback"
		await message.delete
		await channel.send('only links for submissions or feedback examples O.O')

@bot.command(name='feedback')
async def feedback(ctx, arg1, *, content):
	await message.delete()
	if content.length<100:
		await channel.send('you can give better feedback then that, sweeten it up 100+ characters')
	else
		

bot.run(TOKEN)
