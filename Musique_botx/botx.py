import discord
from discord.ext import commands
import yt_dlp as youtube_dl
from decouple import config

DISCORD_TOKEN=config('DISCORD_TOKEN')
print("Bot script started")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready and logged in as {bot.user.name}')
    
@bot.command(name="stop", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
async def dc(self, ctx):
        await self.vc.disconnect()
        
@bot.command(name='play', aliases=['p'])
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    channel = None

    if voice_channel:
        channel = voice_channel
    else:
        await ctx.send("Vous devez être dans un canal vocal pour utiliser cette commande.")

    if channel:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']
            voice_channel = await channel.connect()
            voice_channel.play(discord.FFmpegPCMAudio( url2, executable=r'C:\ffmpeg\bin\ffmpeg.exe', options="-vn"), after=lambda e: print('done', e))
            voice_channel.source = discord.PCMVolumeTransformer(voice_channel.source)
            voice_channel.source.volume = 0.5  # Ajustez le volume selon vos besoins (0.5 = 50%)
            await ctx.send(f'Playing: {info["title"]}')
        
bot.run(DISCORD_TOKEN)