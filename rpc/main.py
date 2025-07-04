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

# options = webdriver.ChromeOptions()
options = webdriver.EdgeOptions()
BASE_DIR = Path(__file__).parent
options.add_extension(str(BASE_DIR / "crx.crx"))

customSongData = {}
customButtonData = []
with open(BASE_DIR / "custom.json", 'r',encoding="utf-8") as file:
    customSongData = json.load(file)

with open(BASE_DIR / "button.json", 'r',encoding="utf-8") as f:
    customButtonData = json.load(f)

client_id = os.getenv('CLIENT_ID') #i only have it this way for a friend to make their git pull life easy / please do not add a client id .env property (please use my id)
if(not client_id):
    client_id = "1099470938891890689"
    
ytApiKey = os.getenv("YOUTUBE_API_KEY")
RPC = None
# workingOnBlockedWifi = False
# if(not workingOnBlockedWifi):
RPC = Presence(client_id)
RPC.connect()
driver = webdriver.Edge(options=options) # i use edge cause it guilt tripped me into using it (not true anymore)
driver.get("https://music.youtube.com")
youtube = build("youtube","v3",developerKey=ytApiKey)
lasturl = ""
# buttonlist=[{"label":"Listen Together","url":"https://spooketti.github.io/YT-RPC/"},
#                     {"label":"Made By Spooketti","url":"https://github.com/spooketti/YT-RPC"}]
buttonlist = customButtonData

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

wasPaused = False
lastTitle = "  "
while True:
    try:
        isPaused = driver.execute_script("return document.querySelector('video').paused;")
        
        if isPaused:
            if not wasPaused:
                RPC.update(
                        details="Currently Paused",
                        large_image="yt_icon",  
                        small_image="pause",   
                        state=lastTitle,
                        buttons=buttonlist,
                        # start=time.time()
                    )
                wasPaused = True
            time.sleep(5)
            continue

        # Only runs if NOT paused
        if lasturl == driver.current_url and not wasPaused:
            time.sleep(5)
            continue

        wasPaused = False  # Reset if no longer paused
        lasturl = driver.current_url

        songID = getVideoId(driver.current_url)
        data = getVideoData(songID)

        thumbnails = data['items'][0]['snippet']['thumbnails']
        imageURL = thumbnails.get('maxres', thumbnails.get('high'))['url']
        imageURL = specialSongImage(songID, imageURL)

        artist = data['items'][0]['snippet']['channelTitle'].replace(" - Topic", "")
        artist = artist.removesuffix("VEVO")
        artist = artistOverride(songID, artist)

        title = data['items'][0]['snippet']['title']
        rawTitle = title #needed for aura loss prevention
        if len(title) <= 2:
            title += "  "
        title = titleOverride(songID, title)
        lastTitle = f"Last Heard: {title}"

        largeText = title
        try:
            largeText = driver.execute_script("const element = document.evaluate(\"//yt-formatted-string[text()='Playing from']\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; return element.nextElementSibling.textContent;")
            largeText = secretAlbumText(songID, largeText)
            if largeText == f"{rawTitle} Radio": #prevention of aura loss
                largeText = title
        except:
            largeText = secretAlbumText(songID, title)
        channelPFP = getChannelPFP(data['items'][0]['snippet']['channelId'])

        currentSongTime = driver.execute_script("return document.querySelector('video').currentTime")
        RPC.update(
                large_image=imageURL,
                small_image=channelPFP,
                state=artist,
                details=title,
                small_text=artist,
                large_text=largeText,
                buttons=buttonlist,
                start=int(time.time() - currentSongTime)
            )

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
        continue

    time.sleep(15)
