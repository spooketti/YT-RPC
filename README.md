# YouTube Music Rich Presence

Broadcast the status of the user's Discord account to showcase what song they are listening to<br>
I created this project based on a personal epiphany: Spotify had too many ads and required a premium subscription to listen together, so I made it possible to listen together for free, along with ad blocking. <br>
The listen together feature currently only works for one streamer globally, but a room system may be implemented.<br>
There is a websocket-based chat system allowing the broadcaster to take requests from their listening audience. 
This project requires you to generate a YouTube API key, specifically the YouTube Data API v3

### Voice Call with Buttons Preview
<img width="346" height="239" alt="image" src="https://github.com/user-attachments/assets/25647dbe-b964-4dd2-b550-5851d5ed7b26" />

### Profile Preview
<img width="365" height="152" alt="image" src="https://github.com/user-attachments/assets/25a64b60-ed46-4246-9bb0-e18b9a331d85" />

### Customization via custom.json
![customgif](https://github.com/user-attachments/assets/5cccfcf3-c715-477a-b952-ee604bd89be3)



# Running YT-RPC

Best works with Python 3.13.9

Navigate to the [Google Cloud developer](https://console.cloud.google.com) console and obtain an api key for the data API, then create a file in the rpc directory named .env with the value YOUTUBE_API_KEY="yourkey"

This project comes with certain songs with custom properties with almost everything being customizable (animated album art, overriding the album name to be a message of your choice, overriding the artist, etc), which is changeable in custom.json

For example
```js
"54Li_V5CUXo":{ //youtube song id findable after the v=, https://music.youtube.com/watch?v=54Li_V5CUXo <----
        "albumText": "", //put a custom message here
        "artist": "Joe Hisaishi", //override the artist's name (in case it's not the artist themselves who posted)
        "albumArt": "https://miro.medium.com/v2/resize:fit:894/1*MnL6k0GSHTm7dMU5XgRDKA.gif", //you can put pngs here but this changes the album art and can be animated on discord
        "title": "Inochi No Kioku", //override the title
        "dev title": "inochi no kioku" //this is just for your own personal sake so you know what matches what
    },
```

Installing Packages
```shell
# navigate to the YT-RPC directory
python -m venv .venv
.venv/Scripts/activate.bat
pip install -r requirements.txt
```

I've personally found YT-RPC to work best by running it through my terminal
<img width="1185" height="367" alt="image" src="https://github.com/user-attachments/assets/49575042-d646-40b3-be29-08d87b7f3c16" />


Here's the bat script i used
```bash
cd "pathtoytrpc/YT-RPC/.venv/Scripts"
call activate.bat
cd ../../rpc
set /p "nodiscord=Run Using Discord? saying no means dont show it as your activity (y/n)"
If /I "%nodiscord%" == "y" (python main.py) ELSE (python main.py --nodiscord)
```

## Folder Documentation
- crx folder: chrome extension that the Selenium browser runs and sends out peerconnection with WebRTC to transfer the music out
- rpc folder: (gitignored .env file with YOUTUBE_API_KEY generated from google's api, run main.py with discord client open to connect to YT-RPC
- server folder: runs on any public webserver
- everything else: runs on the github pages website where people can connect, uses WebRTC to do the listen together mechanic

