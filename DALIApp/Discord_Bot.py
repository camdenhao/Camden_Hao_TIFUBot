import json
import discord
import requests
import praw
import asyncio
import os

from dotenv import load_dotenv
from google.cloud import texttospeech
from google.oauth2 import service_account
from discord.ext import commands
from discord.ext.commands import Bot


#text to speech
credentials = service_account.Credentials.from_service_account_file(r'C:\Users\camde\OneDrive\Desktop\DALIApp\GOOGLE_APPLICATION_CREDENTIALS.json')
TTSclient = texttospeech.TextToSpeechClient(credentials=credentials)
#Build the voice request, select the language code ("en-US") 
#and the ssml voice gender ("neutral")
voice = texttospeech.types.VoiceSelectionParams(language_code = 'en-US', ssml_gender = texttospeech.enums.SsmlVoiceGender.NEUTRAL)

#Select the type of audio file you want returned 
audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    
#reddit stuff

load_dotenv()
client_id1 = os.getenv('CLIENT_ID')
client_secret1= os.getenv('CLIENT_SECRET')
user_agent1 = os.getenv('USER_AGENT')
password1 = os.getenv('PASSWORD')
#username must be manually entered because .env files don't support "_"

token = os.getenv('DISCORD_TOKEN')
reddit = praw.Reddit(client_id = client_id1, client_secret= client_secret1, user_agent = user_agent1, username = 'CH_DALI_TEMP', password = password1)
print('success authenticating!')
reddit.read_only

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name = 'Fun Times')
    print(f'{bot.user.name} has connected to Discord!')
@bot.event 
async def on_member_join(member):
    await member.dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome!')
@bot.command(pass_context = True) 
async def read(ctx, link):
    if 'reddit.com/r/tifu' in link:
        try:
            submission = reddit.submission(url=link)
        except:
            await ctx.send("This isn't a TIFU link")
        print(submission.selftext)
        try:
            #set the text input to be synthesized
            synthesis_input = texttospeech.types.SynthesisInput(text = submission.selftext) #text cannot contain emojis
            #Perform the text-to-speech request on the text input with the selected
            #voice parameters and audio file type
            response = TTSclient.synthesize_speech(synthesis_input, voice, audio_config)
            with open('output.mp3', 'wb') as out:
            # Write the response to the output file.
                out.write(response.audio_content)
                print('Audio content written to file "output.mp3"') 
            if len(bot.voice_clients) == 0: #verifies if bot is in voice channel. If not, then joins the channel the user is in
                vc = await ctx.message.author.voice.channel.connect()
            else:
                vc = bot.voice_clients[0]
                if vc.is_playing():       
                    vc.stop() 
            vc.play(discord.FFmpegPCMAudio(source = 'output.mp3'))
        except:
            await ctx.send("Make sure the text doesn't have any emojis in it or I'll get confused")
    elif message.content == 'raise-exception':
        raise discord.DiscordException
@bot.command(pass_context = True)
async def pause(ctx):
    #check if bot is in a voice channel and playing something
    if len(bot.voice_clients) != 0 and bot.voice_clients[0].is_playing(): 
        await bot.voice_clients[0].pause()
    else:
        await ctx.send("Can't pause this, I'm not playing!")
@bot.command(pass_context = True)
async def resume(ctx):
    #similar to pause()
    if len(bot.voice_clients) != 0 and bot.voice_clients[0].is_paused():
        await bot.voice_clients[0].resume()
    else:
        await ctx.send("..Why are you trying to resume? I'm not even paused")
@bot.command(pass_context = True)
async def join(ctx):
    try:
        if len(bot.voice_clients) != 0:
            await ctx.message.guild.voice_client.disconnect()
        await ctx.message.author.voice.channel.connect()
    except:
        await ctx.send('You must be in a channel for the bot to join you!')
@bot.command(pass_context = True)
async def leave(ctx):
    try:
        server = ctx.message.guild.voice_client
        await server.disconnect()
    except:
        await ctx.send("You can't end what you haven't started")
@bot.command(pass_context = True)
async def exit(ctx):
    await bot.logout()
@bot.command(pass_context = True)
async def stop(ctx):
    if len(bot.voice_clients[0]) != 0:
        await bot.voice_clients[0].stop()
bot.run(token)