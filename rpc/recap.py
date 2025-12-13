import datetime
import json
from pathlib import Path

recapData = {}
BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "recap.json", 'r',encoding="utf-8") as file:
    recapData = json.load(file)
    file.close()

def getDate():
    return str(datetime.datetime.now().date())

def writeSong(songID):
    with open(BASE_DIR / "recap.json", 'w',encoding="utf-8") as file:
        date = getDate()
        if not(date in recapData):
            recapData[date] = {}
        if not(songID in recapData[date]):
            recapData[date][songID] = {
                "plays":0
            }
        recapData[date][songID]["plays"] = int(recapData[date][songID]["plays"]) + 1
        json.dump(recapData,file,indent=4)
