import speech_recognition as sr
import pyttsx3
import requests
import random

from dizio import DIZIO
from executor import wiki, alarm

engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
for voice in voices:
  if ("italian" in voice.id):
    engine.setProperty('voice', voice.id)
    break

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
  engine.say(string)
  engine.runAndWait()

def pick(string):
  return random.choice(DIZIO[string])

def process(command):
  spl = command.split()
  if spl[0] == "cerca" or spl[0] == "cercami":
    return speak(wiki(spl))
  elif spl[0] == "grazie" or (len(spl) > 1 and spl[0] == "ti" and spl[1] == "ringrazio"):
    return speak(pick("prego"))
  elif spl[0] == "metti" or spl[0] == "imposta" or spl[0] == "setta":
    return speak(alarm(spl, engine))
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
