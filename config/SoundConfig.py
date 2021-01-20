from playsound import playsound
import random

Sounds = [
            "./Sounds/insult1.wav"
        ]

soundToPlay = random.choice(Sounds)

def SoundStart():
    playsound(soundToPlay)
