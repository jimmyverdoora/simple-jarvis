import speech_recognition as sr
import requests
import random
from gtts import gTTS
from io import BytesIO
import os
import wave

from dizio import DIZIO
from env import FOLDER, THRESHOLD
from executor import wiki, alarm, ore, meteo

def listen():
  r=sr.Recognizer()
  os.system("/usr/bin/rec " + FOLDER + "tmp.wav trim 0:0 0:10 silence -l 0 1 1.5 " + THRESHOLD)
  statement = None
  with wave.open(FOLDER + "tmp.wav", "rb") as source:    
    try:
      rate = source.getframerate()
      width = source.getsampwidth()
      n = source.getnframes()
      data = source.readframes(n)
      audio = sr.AudioData(data, rate, width*2)
      statement=r.recognize_google(audio, language='it-it')
      print(statement)
    except Exception as e:
      print(e)
      return None
  return statement

def speak(string):
  tts = gTTS(string, lang='it')
  with open(FOLDER + 'tmp.mp3', 'wb') as f:
    tts.write_to_fp(f)
  os.system("/usr/bin/mpg321 " + FOLDER + "tmp.mp3")

def pick(string):
  return random.choice(DIZIO[string])

def process(command):
  spl = command.split()
  if "che ore sono" in " ".join(spl).lower():
    return speak(ore())
  elif "meteo" in spl:
    return speak("mi spiace questa feature è ancora in fase di sviluppo")
  elif spl[0] == "cerca" or spl[0] == "cercami":
    return speak(wiki(spl))
  elif spl[0] == "grazie" or (len(spl) > 1 and spl[0] == "ti" and spl[1] == "ringrazio"):
    return speak(pick("prego"))
  elif spl[0] == "metti" or spl[0] == "imposta" or spl[0] == "setta":
    return speak(alarm(spl, speak))
  elif spl[0] == "spegniti" or spl[0] == "buonanotte":
    speak(pick("buonanotte"))
    return os.system("sudo shutdown -h now")
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
