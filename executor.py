import wikipedia
import datetime
import threading
import time

def wiki(spl):
  wikipedia.set_lang("it")
  if spl[-1] == "google" or spl[-1] == "wikipedia":
    spl = spl[:-1]
    if spl[-1] == "su":
      spl = spl[:-1]
  spl = spl[1:]
  if len(spl) == 0:
    return "Mi spiace, non ho capito cosa cercare"
  results = wikipedia.search(" ".join(spl))
  if len(results) == 0:
    return "Mi spiace, non ho trovato risultati"
  page = wikipedia.page(results[0])
  return page.content.split("==")[0]

def alarm(spl, engine):
  # 2 cases: given interval or given time
  if len(spl) < 2:
    return "Cosa devo impostare?"
  if spl[1] == "un" or spl[1] == "una":
    del spl[1]
  del spl[0]
  if len(spl) < 3:
    return "Cosa devo impostare?"
  numInSec = 0
  if spl[0] == "timer" and spl[1] == "di":
    del spl[1]
    del spl[0]
    if spl[0] == "un'ora":
      spl = ["1"] + spl
      spl[1] = "ore"
    elif spl[0] == "un":
      spl[0] = "1"
    repeat = True 
    if len(spl) < 2:
      if len(spl) == 1 and spl[0] == "mezz'ora":
        numInSec = 1800
        repeat = False
      else:
        return "Un timer di quanto?"
    try:
      while repeat:
        if "mezz" in spl[0]:
          numInSec *= 1.5
          del spl[0]
        else:
          num = int(spl[0])
          if "or" in spl[1]:
            num = num * 3600
          elif "minut" in spl[1]:
            num = num * 60
          elif "second" in spl[1]:
            pass
          else:
            raise Exception("")
          numInSec += num
          del spl[1]
          del spl[0]
        if len(spl) == 0 or spl[0] != "e":
          repeat = False
        else:
          del spl[0]
    except Exception as e:
      print(e)
      return "Un timer di quanto?"
  elif spl[0] == "sveglia" and spl[1] == "alle":
    del spl[1]
    del spl[0]
    ore = 0
    minuti = 0
    try:
      ora = spl[0]
      ora = ora.split(":")
      if len(ora) > 2:
        raise Exception("")
      ore = int(ora[0])
      if len(ora) > 1:
        minuti = int(ora[1])
    except Exception as e:
      print(e)
      return "Una sveglia alle?"
    now = datetime.datetime.now()
    x = datetime.datetime(now.year, now.month, now.day, ore, minuti, 0)
    if (now > x):
      return "Signore, le ore " + str(ore) + " e " + str(minuti) + " sono già passate"
    numInSec = (x-now).seconds
    del spl[0]
  else:
    return "Cosa devo impostare?"
  whatToSay = "bip bip... bip bip... bip bip... "
  if len(spl) > 0 and ("ricorda" in spl[0] or spl[0] == "per"):
    del spl[0]
  if len(spl) > 0 and spl[0] == "di":
    del spl[0]
  if len(spl) > 0:
    whatToSay += "le ricordo di " + " ".join(spl)
  else:
    whatToSay += "sono passati " + str(numInSec) + " secondi"
  return _setAlarm(numInSec, whatToSay, engine)

def _setAlarm(timeInSec, whatToSay, engine):
  def foo():
    time.sleep(timeInSec)
    engine.say(whatToSay)
    engine.runAndWait()
  thr = threading.Thread(target=foo, args=(), kwargs={})
  thr.start()
  print("alarm set in " + str(timeInSec) + "seconds")
  return "Fatto. Ti avviserò fra " + _buildTime(timeInSec)

def _buildTime(sec):
  if sec < 60:
    name = " secondo" if sec == 1 else " secondi"
    return str(sec) + name
  elif sec < 3600:
    m = int(sec/60)
    name = " minuto" if m == 1 else " minuti"
    res = str(m) + name
    if not m == sec * 60:
      name = " secondo" if (sec-60*m == 1) else " secondi"
      res = res + " e " + str(sec-60*m) + name
    return res
  else:
    h = int(sec/3600)
    name = " ora" if h == 1 else " ore"
    res = str(h) + name
    sec -= h*3600
    if sec == 0:
      return res
    m = int(sec/60)
    name = " minuto" if m == 1 else " minuti"
    res = res + " e " + str(m) + name
    if not (m == sec * 60):
      name = " secondo" if (sec-60*m == 1) else " secondi"
      res = res + " e " + str(sec-60*m) + name
    return res