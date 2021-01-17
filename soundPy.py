from playsound import playsound
from configparser import ConfigParser
import time
import json

f = open('./config/config.json', 'r')
data = json.load(f)


time.sleep(5.8)
playsound(data["SoundFile"])
    

