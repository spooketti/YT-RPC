from pypresence import Presence
import webbrowser
import time
from selenium import webdriver
from urllib.parse import urlparse, parse_qs


client_id = '1099470938891890689'  
RPC = Presence(client_id)
RPC.connect()
driver = webdriver.Edge() # i use edge cause it guilt tripped me into using it
driver.get("https://music.youtube.com")

def getThumbnailURL(url):
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get("v", [""])[0]
    return video_id



while True:
    try:
        imageURL = f"https://img.youtube.com/vi/{getThumbnailURL(driver.current_url)}/maxresdefault.jpg"
    except:
        time.sleep(5)
        print("fail")
        continue
    buttonlist=[{"label":"Open Song","url":driver.current_url},
            {"label":"Made By Spooketti","url":"https://github.com/spooketti/YT-RPCZ"}]
    RPC.update(

               large_image=imageURL,
               state="artist name",
               details=driver.title.replace("- YouTube Music", ""),
               buttons=buttonlist
               )
    time.sleep(15) # Can only update rich presence every 15 seconds
    