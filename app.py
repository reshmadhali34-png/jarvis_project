print("Program started")

import cv2
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import pyautogui
import feedparser
import pywhatkit
import customtkinter as ctk
import psutil
import requests
import csv
import random

engine = pyttsx3.init()

contacts = {}

# ---------------- SPEAK ----------------
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ---------------- LISTEN ----------------
def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=5, phrase_time_limit=6)
            command = r.recognize_google(audio)
            print("You said:", command)
            return command.lower()
    except:
        return ""

# ---------------- LOAD CONTACTS ----------------
def load_contacts():
    global contacts
    try:
        with open("contacts.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) >= 2:
                    contacts[row[0].lower()] = row[1]
        speak("Contacts loaded")
    except:
        speak("Error loading contacts")

# ---------------- WEATHER ----------------
def weather(cmd):
    city = cmd.replace("weather in", "").strip()
    if city == "":
        speak("Say weather in city name")
        return
    data = requests.get(f"https://wttr.in/{city}?format=3").text
    speak(data)

# ---------------- SCREENSHOT ----------------
def screenshot():
    pyautogui.screenshot().save("shot.png")
    speak("Screenshot saved")

# ---------------- CALCULATOR ----------------
def calculate(cmd):
    try:
        expr = cmd.replace("calculate", "").replace("x", "*")
        result = eval(expr)
        speak(f"Result is {result}")
    except:
        speak("Invalid calculation")

# ---------------- SONG ----------------
def play_song(cmd):
    query = cmd.replace("play", "")
    webbrowser.open(f"https://youtube.com/results?search_query={query}")
    speak("Playing on YouTube")

# ---------------- WHATSAPP ----------------
def whatsapp(cmd):
    try:
        cmd = cmd.replace("send message to", "").replace("whatsapp", "").strip()
        name = cmd.split()[0]
        msg = " ".join(cmd.split()[1:])

        if name in contacts:
            pywhatkit.sendwhatmsg_instantly(contacts[name], msg)
            speak("Message sent")
        else:
            speak("Contact not found")
    except:
        speak("WhatsApp failed")

# ---------------- SYSTEM STATUS ----------------
def system():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    speak(f"CPU {cpu} RAM {ram}")

# ---------------- NEWS ----------------
def news():
    speak("Hindi or English?")
    lang = listen()

    url = "https://news.google.com/rss?hl=hi&gl=IN&ceid=IN:hi" if "hindi" in lang else "https://news.google.com/rss"

    feed = feedparser.parse(url)

    for i in feed.entries[:5]:
        speak(i.title)

# ---------------- GUI ----------------
def gui():
    app = ctk.CTk()
    app.geometry("800x500")
    app.title("Jarvis AI")

    ctk.CTkLabel(app, text="JARVIS DASHBOARD", font=("Arial", 25)).pack(pady=20)

    ctk.CTkButton(app, text="Weather", command=lambda: weather("weather in delhi")).pack(pady=10)
    ctk.CTkButton(app, text="News", command=news).pack(pady=10)
    ctk.CTkButton(app, text="Screenshot", command=screenshot).pack(pady=10)
    ctk.CTkButton(app, text="Google", command=lambda: webbrowser.open("https://google.com")).pack(pady=10)

    app.mainloop()

# ---------------- FACE LOGIN ----------------
def face_login():
    speak("Scanning face")

    rec = cv2.face.LBPHFaceRecognizer_create()
    rec.read("trainer/model.yml")

    face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            id, conf = rec.predict(gray[y:y+h, x:x+w])

            if conf < 70:
                speak("Welcome user")
                cap.release()
                cv2.destroyAllWindows()
                return True

        cv2.imshow("Face Login", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return False

# ---------------- START ----------------
if face_login():
    load_contacts()
    speak("Jarvis Ready")
else:
    speak("Access denied")
    exit()

# ---------------- MAIN LOOP ----------------
while True:
    cmd = listen()

    if cmd == "":
        continue

    if "hello" in cmd:
        speak("Hello")

    elif "weather" in cmd:
        weather(cmd)

    elif "time" in cmd:
        speak(datetime.datetime.now().strftime("%H:%M:%S"))

    elif "date" in cmd:
        speak(datetime.datetime.now().strftime("%d %B %Y"))

    elif "youtube" in cmd:
        webbrowser.open("https://youtube.com")

    elif "google" in cmd:
        webbrowser.open("https://google.com")

    elif "notepad" in cmd:
        os.system("notepad")

    elif "calculator" in cmd:
        os.system("calc")

    elif "screenshot" in cmd:
        screenshot()

    elif "play" in cmd:
        play_song(cmd)

    elif "whatsapp" in cmd:
        whatsapp(cmd)

    elif "news" in cmd:
        news()

    elif "system" in cmd:
        system()

    elif "dashboard" in cmd:
        gui()

    elif "exit" in cmd:
        speak("Goodbye")
        break

    else:
        speak("Sorry, I did not understand")