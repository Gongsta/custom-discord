from discord.ext import commands
import discord
from datetime import datetime
from config import TOKEN
import youtube_dl
client = commands.Bot(command_prefix='.')

#From https://stackoverflow.com/questions/56060614/how-to-make-a-discord-bot-play-youtube-audio
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


@client.command()
async def hello(ctx):
    await ctx.send("Hello!")

@client.command()
async def attendance(ctx):
    channel = ctx.message.author.voice.channel
    members = channel.members

    memberList = ""

    date = datetime.now().strftime("%d-%m-%Y")
    dirname = f"data/{date}.csv"

    with open(dirname, "w") as file:
        for member in members:
            memberList += (member.name + "#" + member.discriminator + "\n")
            file.write(member.name + "#" + member.discriminator + '\n')

    await ctx.send(memberList)


@client.command()
async def connect(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()


#pip install youtube_dl
@client.command()
async def play(ctx, args):
    #Args is a url
    print(args)
    async with ctx.typing():
        player = await YTDLSource.from_url(args, loop=ctx.bot.loop)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    await ctx.send('Now playing: {}'.format(player.title))

@client.command()
async def disconnect(ctx):
    await ctx.voice_client.disconnect()


# @client.command()
# async def pins(ctx):
#     await ctx.send(ctx.pins())

@client.command()
async def close(ctx):
    ctx.send("Closing bot")
    await client.close()



client.run(TOKEN)