# Youtube Music Rich Presence

This project will not work natively just by downloading the files as it is rigged up to only work on my account

But:

crx folder: chrome extension that the Selenium browser runs and sends out peerconnection with WebRTC to transfer the music out
if you are to trying to make this work for you: go to chrome://extensions and then pack the crx folder into an extension

(gitignored) private folder in rpc directory: crx.crx and the pem file

rpc folder: (gitignored .env file with YOUTUBE_API_KEY generated from google's api and CLIENT_ID of the discord application), run main.py with discord client open to connect to YT-RPC

server folder: runs on any public webserver

everything else: runs on the github pages website where people can connect, uses WebRTC to do the listen together mechanic

