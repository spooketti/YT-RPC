from pypresence import Presence
import time
from selenium import webdriver
# from selenium.webdriver.edge.options import Options
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from googleapiclient.discovery import build
from pathlib import Path
# import websockets
# import asyncio
import json
import os
load_dotenv()

options = webdriver.ChromeOptions()
BASE_DIR = Path(__file__).parent
options.add_extension(str(BASE_DIR / "crx.crx"))

customSongData = {}
with open(BASE_DIR / "custom.json", 'r',encoding="utf-8") as file:
    customSongData = json.load(file)

client_id = os.getenv('CLIENT_ID') #i only have it this way for a friend to make their git pull life easy / please do not add a client id .env property (please use my id)
if(not client_id):
    client_id = "1099470938891890689"
    
ytApiKey = os.getenv("YOUTUBE_API_KEY")
RPC = None
workingOnBlockedWifi = False
if(not workingOnBlockedWifi):
    RPC = Presence(client_id)
    RPC.connect()
driver = webdriver.Chrome(options=options) # i use edge cause it guilt tripped me into using it (not true anymore)
driver.get("https://music.youtube.com")
youtube = build("youtube","v3",developerKey=ytApiKey)
lasturl = ""
buttonlist=[{"label":"Listen Together","url":"https://spooketti.github.io/YT-RPC/"},
                    {"label":"Made By Spooketti","url":"https://github.com/spooketti/YT-RPC"}]

def getVideoData(vidId):
    request = youtube.videos().list(part="snippet", id=vidId)
    response = request.execute()
    return response

def getVideoId(url):
    #imageURL = f"https://img.youtube.com/vi/{getThumbnailURL(driver.current_url)}/maxresdefault.jpg" #fun trick this gets it as image no api needed
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get("v", [""])[0]
    return video_id

def getChannelPFP(channelID):
    request = youtube.channels().list(part="snippet",id=channelID)
    response = request.execute()
    return response['items'][0]['snippet']['thumbnails']['default']['url']

def specialSongImage(songID,imageURL):
    return customSongData.get(songID, {}).get("albumArt", "") or imageURL

def secretAlbumText(songID,notInSecretText):
    return customSongData.get(songID, {}).get("albumText", "") or notInSecretText

def artistOverride(songID,artist):
    return customSongData.get(songID, {}).get("artist", "") or artist
    
def titleOverride(songID,title):
    return customSongData.get(songID, {}).get("title", "") or title

wasPaused = False #i ngl have 0 clue why the wasPaused system even works so if anyone could tell me how
#i would aprpeicate this: this litearlly should nto work but it does

kateMode = bool(os.getenv("KATE_MODE")) #ignore this: for a friend

while True:
            if(kateMode):
                buttonlist=[{"label":"Listen To This Song","url":driver.current_url},
                    {"label":"Made By Spooketti","url":"https://github.com/spooketti/YT-RPC"}]
            if(lasturl==driver.current_url and not wasPaused):
                if(driver.execute_script("let video = document.querySelector('video'); return video ? video.paused : null;")):
                    RPC.update(large_image="  ",
                    small_image="  ",
                    state="  ",
                    details="Currently Paused",
                    small_text="  ",
                    large_text="  ",
                    buttons=buttonlist,)
                    wasPaused = True
                    time.sleep(10)
                time.sleep(5)
                continue
            wasPaused = False
            lasturl = driver.current_url
            imageURL=""
            artist=""
            title=""
            channelPFP = ""
            largeText = ""
            try:
                songID = getVideoId(driver.current_url)
                data = getVideoData(songID)
                if("maxres" in data['items'][0]['snippet']['thumbnails']):
                    imageURL = specialSongImage(songID,data['items'][0]['snippet']['thumbnails']['maxres']['url'])
                else:
                    imageURL = specialSongImage(songID,data['items'][0]['snippet']['thumbnails']['high']['url'])
                artist = data['items'][0]['snippet']['channelTitle']
                artist = artist.replace(" - Topic", "")
                artist = artistOverride(songID,artist)
                title = data['items'][0]['snippet']['title']
                if(len(title) <= 2):
                    title += "  "
                title = titleOverride(songID,title)
                largeText = secretAlbumText(songID,title)
                channelPFP = getChannelPFP(data['items'][0]['snippet']['channelId'])
                # await ws.send(json.dumps({"context":"artUpdate","title":title,"artist":artist,"imageURL":imageURL}))
                
            except Exception as e:
                # print(e)
                time.sleep(5)
                continue
            if(not workingOnBlockedWifi):
                RPC.update(

                    large_image=imageURL,
                    small_image=channelPFP,
                    state=artist,
                    details=title,
                    small_text=artist,
                    large_text=largeText,
                    buttons=buttonlist,
                    # party_size=[0,5], #listen together party size,
                    # party_id="YT-RPC"
                    )
            time.sleep(15) # Can only update rich presence every 15 seconds
            #honest to god i need to commit something to save myself in csa im sorry
            