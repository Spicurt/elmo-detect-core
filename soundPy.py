from playsound import playsound
from configparser import ConfigParser
import time

parser = ConfigParser()
parser.read('./config/config.ini')

while True:
    time.sleep(5.8)
    playsound(parser.get("settings", "soundfile"))
    

