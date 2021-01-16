# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

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
@bot.command(name='feedback')
async def feedback(ctx, arg1, arg2, arg3):
	member=ctx.author
	a=arg1
	b=arg2
	c=arg3
	channel = bot.get_channel(800005895026901002)
	await channel.send("artist:{member.name} \nsong:%s \ndescription:%s %s", a,b,c)

@client.event
async def on_message(message):
	key='~feedback'
	if key in message.content:
		await message.delete()

#@bot.command(name='submit')
#async def submit(ctx, arg1, arg2):


bot.run(TOKEN)
