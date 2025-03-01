from pypresence import Presence
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from googleapiclient.discovery import build
import os
load_dotenv()

options = webdriver.EdgeOptions()
options.add_extension("./crx/private/crx.crx")
client_id = os.getenv('CLIENT_ID')
ytApiKey = os.getenv("YOUTUBE_API_KEY")
RPC = None
workingOnBlockedWifi = False
if(not workingOnBlockedWifi):
    RPC = Presence(client_id)
    RPC.connect()
driver = webdriver.Edge(options=options) # i use edge cause it guilt tripped me into using it
driver.get("https://music.youtube.com")
youtube = build("youtube","v3",developerKey=ytApiKey)
lasturl = ""

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

def specialSongImage(imageURL):
    specialAlbumArt = {"https://i.ytimg.com/vi/NtVQkUdyapw/maxresdefault.jpg":"https://media.tenor.com  /qnEtsD44mkQAAAAM/ricky-montgomery-montgomery-ricky.gif", #mr loverman
                       "https://i.ytimg.com/vi/k7kzc3Nof08/maxresdefault.jpg":"https://media.tenor.com/ATdTvm5YQw0AAAAM/roblox-car-crash.gif", #i love you so
                       "https://i.ytimg.com/vi/8KoyWSzcWqU/maxresdefault.jpg":"https://i.imgflip.com/9lkvtr.gif", #she wants me to be loved
                       "https://i.ytimg.com/vi/6P-43ukn_l0/maxresdefault.jpg":"https://i.makeagif.com/media/2-28-2025/f5vwkz.gif", #cancer
                       "https://i.ytimg.com/vi/gm-Y9idMMQ4/maxresdefault.jpg":"https://media.tenor.com/bZrOdhRikM0AAAAM/coldplay-a-rush-of-blood-to-the-head.gif"} #the scientist
    if(imageURL in specialAlbumArt):
        return specialAlbumArt[imageURL]
    return imageURL
    
    

while True:
    if(lasturl==driver.current_url):
        time.sleep(5)
        continue
    lasturl = driver.current_url
    imageURL=""
    arist=""
    title=""
    channelPFP = ""
    try:
        data = getVideoData(getVideoId(driver.current_url))
        imageURL = specialSongImage(data['items'][0]['snippet']['thumbnails']['maxres']['url'])
        artist = data['items'][0]['snippet']['channelTitle']
        title = data['items'][0]['snippet']['title']
        channelPFP = getChannelPFP(data['items'][0]['snippet']['channelId'])
        
    except:
        time.sleep(5)
        continue
    buttonlist=[{"label":"Open Song","url":driver.current_url},
            {"label":"Made By Spooketti","url":"https://github.com/spooketti/YT-RPC"}]
    if(not workingOnBlockedWifi):
        RPC.update(

               large_image=imageURL,
               small_image=channelPFP,
               state=artist,
               details=title,
               buttons=buttonlist,
               )
    time.sleep(15) # Can only update rich presence every 15 seconds
    