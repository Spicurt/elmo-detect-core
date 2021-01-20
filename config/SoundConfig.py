from playsound import playsound
import random

Sounds = [
            "./Sounds/insult1.wav"
        ]



def SoundStart():
    soundToPlay = random.choice(Sounds)
    playsound(soundToPlay)

def helloElmo():
    playsound("./Sounds/hielmo.wav")