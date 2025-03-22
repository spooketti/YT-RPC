from pypresence import Presence
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from googleapiclient.discovery import build
# import websockets
# import asyncio
# import json
import os
load_dotenv()

options = webdriver.EdgeOptions()
options.add_extension("./private/crx.crx")
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
    specialAlbumArt = {"https://i.ytimg.com/vi/NtVQkUdyapw/maxresdefault.jpg":"https://media.tenor.com/qnEtsD44mkQAAAAM/ricky-montgomery-montgomery-ricky.gif", #mr loverman
                       "https://i.ytimg.com/vi/k7kzc3Nof08/maxresdefault.jpg":"https://media.tenor.com/ATdTvm5YQw0AAAAM/roblox-car-crash.gif", #i love you so
                       "https://i.ytimg.com/vi/8KoyWSzcWqU/maxresdefault.jpg":"https://i.imgflip.com/9lkvtr.gif", #she wants me to be loved
                       "https://i.ytimg.com/vi/6P-43ukn_l0/maxresdefault.jpg":"https://i.makeagif.com/media/2-28-2025/f5vwkz.gif", #cancer
                       "https://i.ytimg.com/vi/gm-Y9idMMQ4/maxresdefault.jpg":"https://media.tenor.com/bZrOdhRikM0AAAAM/coldplay-a-rush-of-blood-to-the-head.gif", #the scientist
                       "https://i.ytimg.com/vi/6LEs1yKXnb8/maxresdefault.jpg":"https://i.makeagif.com/media/3-07-2025/SleHgO.gif",#tek it
                       "https://i.ytimg.com/vi/9r0EqOIELbs/maxresdefault.jpg":"https://i.makeagif.com/media/3-07-2025/Lmf04v.gif",#keshi blue even though u cna hardly tell
                       "https://i.ytimg.com/vi/VfBswbj1824/maxresdefault.jpg":"https://media.tenor.com/VM10Cu2CKXEAAAAC/lagtrain-anime.gif", #lagtrain 
                       "https://i.ytimg.com/vi/TxpVLoYDgwo/maxresdefault.jpg":"https://i.makeagif.com/media/3-07-2025/svlz_X.gif", #laufey lovesick
                       "https://i.ytimg.com/vi/GYlL6HjTQgk/hqdefault.jpg":"https://c.tenor.com/2xTyEWuuWvUAAAAd/tenor.gif", #shiwasenara
                        "https://i.ytimg.com/vi/aHmg0jsmNhg/maxresdefault.jpg":"https://images.genius.com/f83b0048db86544e0eb6e45e8551b02e.382x382x249.gif", #vampire
                        "https://i.ytimg.com/vi/3hgabcFcp4A/maxresdefault.jpg":"https://media1.tenor.com/m/NgWUl-LbntoAAAAd/invincible-fly.gif", #feel it
                        "https://i.ytimg.com/vi/dhd_wb7kJB4/hqdefault.jpg":"https://i.makeagif.com/media/3-19-2025/SecNmN.gif"} #kimi no taion
    if(imageURL in specialAlbumArt):
        return specialAlbumArt[imageURL]
    return imageURL

def secretAlbumText(songID,notInSecretText):
    speicalAlbumSecret = {"GYlL6HjTQgk":"as long as you're happy, LW",#shiwasenara
                          "TxpVLoYDgwo":"what have you done to me?", #lovesick
                          "3hgabcFcp4A":"I JUST LOVE THE WAY YOU GOT ME FEEELIN", #feel it
                          "OZYd9JxithE":"i know you're not sorry, why should you be?"} #8

    if(songID in speicalAlbumSecret):
        return speicalAlbumSecret[songID]
    return notInSecretText

def artistOverride(songID,artist):
    override = {"GYlL6HjTQgk":"Goro Majima",#shiwasenara
                "dhd_wb7kJB4":"Kuwagata-P"} #kimi no taion

    if(songID in override):
        return override[songID]
    return artist
    
def titleOverride(songID,title):
    overrideTitle = {"dhd_wb7kJB4":"Kimi no Taion"} #kimi no taion

    if(songID in overrideTitle):
        return overrideTitle[songID]
    return title

while True:
            if(lasturl==driver.current_url):
                time.sleep(5)
                continue
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
                    imageURL = specialSongImage(data['items'][0]['snippet']['thumbnails']['maxres']['url'])
                else:
                    imageURL = specialSongImage(data['items'][0]['snippet']['thumbnails']['high']['url'])
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
            buttonlist=[{"label":"Listen Together","url":"https://spooketti.github.io/YT-RPC/"},
                    {"label":"Made By Spooketti","url":"https://github.com/spooketti/YT-RPC"}]
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
            