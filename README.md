# YouTube Music Rich Presence
Broadcast the status of the user's Discord account to showcase what song they are listening to<br>
I created this project based on a personal epiphany: Spotify had too many ads and required a premium subscription to listen together, so I made it possible to listen together for free, along with ad blocking. <br>
The listen together feature currently only works for one streamer globally, but a room system may be implemented.<br>
There is a websocket-based chat system allowing the braodcaster to take requests from their listening audience. 
This project requires you to generate a YouTube API key, specifically the YouTube Data API v3

### Voice Call with Buttons Preview
<img width="346" height="239" alt="image" src="https://github.com/user-attachments/assets/25647dbe-b964-4dd2-b550-5851d5ed7b26" />

### Profile Preview
<img width="365" height="152" alt="image" src="https://github.com/user-attachments/assets/25a64b60-ed46-4246-9bb0-e18b9a331d85" />

### Customization via custom.json
![customgif](https://github.com/user-attachments/assets/5cccfcf3-c715-477a-b952-ee604bd89be3)



# Running YT-RPC
Navigate to the Google Cloud developer console and obtain an api key for the data API, then create a file into rpc named .env with the value YOUTUBE_API_KEY="yourkey"
This project comes with certain songs with custom properties such as a hover text or custom animated album art, which is changeable in custom.json
Either open YT-RPC in a code editor of your choice and run main.py in the rpc folder (only use this for development purposes such as previewing custom.json changes) <br>
Albiet untested, running the script raw with Python<br>
Or compile YT-RPC into an exe using pyinstaller

## Folder Documentation
- crx folder: chrome extension that the Selenium browser runs and sends out peerconnection with WebRTC to transfer the music out
- rpc folder: (gitignored .env file with YOUTUBE_API_KEY generated from google's api, run main.py with discord client open to connect to YT-RPC
- server folder: runs on any public webserver
- everything else: runs on the github pages website where people can connect, uses WebRTC to do the listen together mechanic

