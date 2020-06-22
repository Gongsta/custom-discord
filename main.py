import discord
from datetime import datetime
from config import TOKEN

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    #message.channel
    #message.author
    #message.author.name
    #message.content

    print(message.author, ":", message.content)

    if message.content.startswith('.hello'):
        await message.channel.send('Hello!')


    if message.content == ".close":
        await client.close()

    if message.content == ".attendance":
        channel = message.author.voice.channel
        members = channel.members

        memberList = ""

        date = datetime.now().strftime("%d-%m-%Y")
        dirname = f"data/{date}.csv"

        with open(dirname, "w") as file:
            for member in members:
                memberList += (member.name + "#" + member.discriminator + "\n")
                file.write(member.name + "#" + member.discriminator + '\n')
                file.write("John Cena" + "#" + member.discriminator + '\n')


        await message.channel.send(memberList)




client.run(TOKEN)