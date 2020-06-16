from discord.ext import commands
import discord
from config import TOKEN
client = commands.Bot(command_prefix='.')

@client.command()
async def attendance(ctx):
    channel = ctx.message.author.voice.channel
    members = channel.members


    for member in members:
        print(member.name + "#" + member.discriminator)
        await ctx.send(member.name + "#" + member.discriminator)



@client.command()
async def connect(ctx):
    channel = ctx.message.author.voice.channel
    channel.connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()



client.run(TOKEN)