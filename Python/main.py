import os
import struct
import sys
import time
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
from gtts import gTTS
import http.client
import http.server
import http
import json
import requests
import commands
import spotifyCode
import webbrowser
import struct
import pyaudio
import pvporcupine

ready = False
Wakeword = False

#Spotify activation

spotifyResult = spotifyCode.data(webbrowser, ready, requests, json)
SpotifyToken = spotifyResult[0]
SpotifyDeviceID = spotifyResult[1]
ready = spotifyResult[2]
DeviceList = spotifyResult[3]

# allows to run this script on windows
if not os.name == "nt":
  from pixel_ring import pixel_ring
  from gpiozero import LED

  power = LED(5)
  power.on()
  pixel_ring.set_brightness(10)

#----

def speak(text):
    tts = gTTS(text=text, lang="de")
    filename = "voice.mp3"
    tts.save(filename)

    song = AudioSegment.from_mp3(filename)
    play(song)

def recognition():
  recognitionText = ""
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Say something!")
    print()
    audio = r.listen(source)
      
  try:
    recognitionText = r.recognize_google(audio, language='de-DE')
    print(recognitionText)
  except:
    pass
  return recognitionText.lower()

#Answers

try:
  while ready == True:
    Text = recognition()
    SpeechText = ""

    if "raspberry" in Text:
      if not os.name == "nt":
        pixel_ring.wakeup()
      Wakeword = True
    
    if Wakeword == True:
      Text = recognition()
      if "was geht" in Text:
        SpeechText = commands.was_geht()
      elif "danke" in Text:
        SpeechText = commands.danke()
      elif "ich bin so gut" in Text:
        SpeechText = commands.gut()
      elif "sag meinem lehrer mal wie viel uhr es ist" in Text or "wie viel uhr ist es" in Text or "uhrzeit" in Text or "wie viel uhr ist es gerade" in Text or "wie spät ist es" in Text:
        SpeechText = commands.uhrzeit(time)
      elif "datum" in Text:
        SpeechText = commands.datum(time)
      elif "mach einen backflip" in Text:
        SpeechText = commands.backflip()
      elif "pausiere meine musik" in Text or  "spotify pause" in Text:
        try:
          SpeechText = commands.spotify_pause(SpotifyToken, SpotifyDeviceID, requests)
        except:
          print("Spotify Error")
          spotifyResult = spotifyCode.data(webbrowser, ready, requests, json)
          SpotifyToken = spotifyResult[0]
          SpotifyDeviceID = spotifyResult[1]
          ready = spotifyResult[2]
          DeviceList = spotifyResult[3]
      elif  "setze meine musik fort" in Text or  "setze musik fort" in Text or  "setze meine musik vor" in Text or  "meine musik fort" in Text or "spotify play" in Text:
        try:
          SpeechText = commands.spotify_play(SpotifyToken, SpotifyDeviceID, requests)
        except:
          spotifyResult = spotifyCode.data(webbrowser, ready, requests, json)
          SpotifyToken = spotifyResult[0]
          SpotifyDeviceID = spotifyResult[1]
          ready = spotifyResult[2]
          DeviceList = spotifyResult[3]
      elif "spotify skip" in Text or "überspringe diesen song" in Text or "überspringe den track" in Text or "überspringen track" in Text or "überspring den dreck" in Text or "überspringe den dreck" in Text or "überspringen dreck" in Text:
        try:
          SpeechText = commands.spotify_skip(SpotifyToken, SpotifyDeviceID, requests)
        except:
          print("Spotify Error")
          spotifyResult = spotifyCode.data(webbrowser, ready, requests, json)
          SpotifyToken = spotifyResult[0]
          SpotifyDeviceID = spotifyResult[1]
          ready = spotifyResult[2]
          DeviceList = spotifyResult[3]
      elif "zeig mir meine verfügbaren Geräte auf Spotify" in Text or "spotify geräte" in Text:
        SpeechText = commands.spotify_devices(SpotifyToken, SpotifyDeviceID, requests, DeviceList, json)
      elif "fick dich" in Text:
        SpeechText = "Ha hahaha aha ha"
      elif "verpissdich" in Text:
        speak("O O O O O O O O O")
        exit()
      else:
        #SpeechText = commands.error()
        print("Ich konnte dich nicht verstehen!")

      Text = ""

      try:
        if not os.name == "nt":
          pixel_ring.think()
        if SpeechText != "":
          speak(SpeechText)
          

        if not os.name == "nt":
          pixel_ring.off()
      except Exception as e:
        print("Error")
      Wakeword = False
    else:
      if not os.name == "nt":
        pixel_ring.off()
except:
  pass

power.off()