# Camden_Hao_TIFUBot
A discord bot that utilizes Google's TTS API and the Reddit API to read posts from r/TIFU out loud. 



Setting up environment: 

make sure pip is downloaded: https://bootstrap.pypa.io/get-pip.py

Enter in command prompt: 

-python get-pip.py 

-pip install python-dotenv //for getting credentials 

-pip install praw //Reddit API wrapper 

-pip install -U git+https://github.com/Rapptz/discord.py@master#egg=discord.py[voice] //discord.py version 1.3.0a, make sure you have git

-pip install asyncio //allows await/async syntax in code 

-pip install --upgrade google-cloud-texttospeech

-pip install -U python-dotenv 



-install ffmpeg https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg

//Make sure to add file path to 'ffmpeg.exe' in PATH in environment variables 


Throaway Discord Account for testing: 

Username: CH_DALI_TEMP - Login email: ch.baccaman@gmail.com

Password: dalilab20w





Commands (precede with '.')

-join //joins voice channel you are in 

-leave //leaves voice channel 

-logout //disconnects bot from server and ends code run 

-read (link) //checks if is reddit/TIFU post, then reads the post 

-pause //pauses reading

-resume //resumes reading


IMPORTANT
This bot requires the correct .env and GOOGLE_APPLICATION_VERIFICATION.json file. Which I must send to you. Put it in the DALIApp folder in order for the bot to work

Make sure .env file is only called '.env'. This may get messed when sent.

*Inside code change the line* 

credentials = service_account.Credentials.from_service_account_file(r'C:\Users\camde\OneDrive\Desktop\DALIApp\GOOGLE_APPLICATION_CREDENTIALS.json') to the path to the included google verification json file

