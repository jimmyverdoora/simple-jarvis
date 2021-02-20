import speech_recognition as sr
import requests
import random
from gtts import gTTS
from io import BytesIO
import os

from dizio import DIZIO
from executor import wiki, alarm

def listen():
  r=sr.Recognizer()
  r.dynamic_energy_threshold = False
  r.energy_threshold = 300
  with sr.Microphone() as source:    
    try:
      audio=r.listen(source, timeout=10.0)
      statement=r.recognize_google(audio, language='it-it')
      print(statement)
    except Exception as e:
      return None
    return statement

def speak(string):
  tts = gTTS(string, lang='it')
  with open('tmp.mp3', 'wb') as f:
    tts.write_to_fp(f)
  os.system("/usr/bin/mpg321 /home/pi/simple-jarvis/tmp.mp3")

def pick(string):
  return random.choice(DIZIO[string])

def process(command):
  spl = command.split()
  if spl[0] == "cerca" or spl[0] == "cercami":
    return speak(wiki(spl))
  elif spl[0] == "grazie" or (len(spl) > 1 and spl[0] == "ti" and spl[1] == "ringrazio"):
    return speak(pick("prego"))
  elif spl[0] == "metti" or spl[0] == "imposta" or spl[0] == "setta":
    return speak(alarm(spl, speak))
  elif spl[0] == "spegniti" or spl[0] == "buonanotte":
    speak(pick("buonanotte"))
    return # todo: shutdown
  else:
    speak(pick("ripeti"))
  return

if __name__=='__main__':

  speak(pick("greetings"))
  isTriggered = False # quando lo chiami per nome lo attivi

  while True:
    print(isTriggered)
    statement = listen()
    if statement is not None:
      if "jarvis" in statement.lower().split(" "):
        if not isTriggered:
          speak(pick("dimmi"))
          isTriggered = True
        elif isTriggered:
          process(statement.lower())
      elif isTriggered:
        process(statement.lower())
    else:
      isTriggered = False
