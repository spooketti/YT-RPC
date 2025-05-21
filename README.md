# YouTube Music Rich Presence
Broadcast the status of the user's Discord to showcase what song they are listening to
I made this project out of a personal epiphany with Spotify having too many ads and requiring premium to listen together, so listen together comes free alongside ad block. 
The listen together feature currently only works for one streamer globally, but a room system may be implemented.
This project requires you to generate a YouTube API key, specifically the YouTube Data API v3

![image](https://github.com/user-attachments/assets/c63aa9cb-9988-4080-964c-ae01e20ddf24)


# Running YT-RPC
Navigate to the Google Cloud developer console and obtain an api key for the data API, then create a file into rpc and create a .env file with the value YOUTUBE_API_KEY="yourkey"
This project comes with certain songs with custom properties such as a hover text or custom animated album art, which is changeable in custom.json
Either open YT-RPC in a code editor of your choice and run main.py in the rpc folder (only use this for development purposes such as previewing custom.json changes)
Or compile YT-RPC into an exe using pyinstaller

## Folder Documentation
- crx folder: chrome extension that the Selenium browser runs and sends out peerconnection with WebRTC to transfer the music out
- rpc folder: (gitignored .env file with YOUTUBE_API_KEY generated from google's api, run main.py with discord client open to connect to YT-RPC
- server folder: runs on any public webserver
- everything else: runs on the github pages website where people can connect, uses WebRTC to do the listen together mechanic

