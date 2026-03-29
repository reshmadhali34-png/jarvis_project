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
import psutil
import requests
import csv
import time
import threading
import winsound
import re

engine = pyttsx3.init()
contacts = {}

# 🔊 SPEAK
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# 🎤 LISTEN
def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.energy_threshold = 300
            audio = r.listen(source, timeout=5, phrase_time_limit=6)
            command = r.recognize_google(audio)
            print("You said:", command)
            return command.lower()
    except:
        return ""

# 📒 LOAD CONTACTS
def load_contacts():
    global contacts
    try:
        with open("contacts.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                contacts[row[0].strip().lower()] = row[1].strip()
        speak("Contacts loaded successfully")
    except:
        speak("Error loading contacts file")

# 🌦 WEATHER
def get_weather_from_command(command):
    try:
        if "in" in command:
            city = command.split("in")[-1].strip()
        else:
            speak("Say like weather in Delhi")
            return

        url = f"https://wttr.in/{city}?format=j1"
        data = requests.get(url).json()

        temp = data["current_condition"][0]["temp_C"]
        desc = data["current_condition"][0]["weatherDesc"][0]["value"]

        speak(f"{city} weather is {desc} with temperature {temp}°C")
    except:
        speak("Unable to fetch weather")

# 📸 SCREENSHOT
def take_screenshot():
    pyautogui.screenshot().save("screenshot.png")
    speak("Screenshot taken")

# 🧮 CALCULATOR
def calculate(command):
    try:
        expr = command.replace("calculate", "").strip().replace("x", "*")
        if expr == "":
            speak("What should I calculate?")
            expr = listen()
        result = eval(expr)
        speak(f"Result is {result}")
    except:
        speak("Cannot calculate")

# 🎵 SONG
def play_song(command):
    try:
        query = command.replace("play", "").strip()
        if query == "":
            speak("Which song?")
            query = listen()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    except:
        speak("Cannot play song")

# 📱 WHATSAPP
def send_whatsapp(command):
    try:
        command = command.lower()
        for word in ["send whatsapp to", "send message to", "whatsapp", "message"]:
            command = command.replace(word, "")
        words = command.strip().split()

        if len(words) < 2:
            speak("Say name and message")
            return

        name = words[0]
        message = " ".join(words[1:])

        if name not in contacts:
            speak("Contact not found")
            return

        pywhatkit.sendwhatmsg_instantly(contacts[name], message)
        speak("Message sent")
    except:
        speak("WhatsApp failed")

# 💻 SYSTEM STATUS
def system_status():
    speak(f"CPU {psutil.cpu_percent()} percent, RAM {psutil.virtual_memory().percent} percent")

# 📰 NEWS
def get_news():
    try:
        speak("Hindi or English?")
        lang = listen()
        url = "https://news.google.com/rss?hl=hi&gl=IN&ceid=IN:hi" if "hindi" in lang else "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        news = feedparser.parse(url)
        for n in news.entries[:5]:
            speak(n.title)
    except:
        speak("News error")

# ⏰ SMART ALARM
def set_alarm(command):
    try:
        match = re.search(r'\d{1,2}:\d{2}\s?(am|pm)?', command)
        if not match:
            speak("Say time like 7:30 or 7:30 am")
            return

        time_str = match.group()
        alarm_time = datetime.datetime.strptime(
            time_str, "%I:%M %p" if "am" in time_str or "pm" in time_str else "%H:%M"
        ).time()

        speak(f"Alarm set for {time_str}")

        def alarm():
            while True:
                now = datetime.datetime.now().time()
                if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
                    speak("Wake up Reshma!")
                    for _ in range(5):
                        winsound.Beep(1000, 1000)
                    break
                time.sleep(20)

        threading.Thread(target=alarm).start()
    except:
        speak("Alarm error")

# 🔐 FACE LOGIN
def face_login():
    speak("Scanning face")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer/model.yml")

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            _, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            if confidence < 70:
                speak("Welcome Reshma")
                cap.release()
                cv2.destroyAllWindows()
                return True

        cv2.imshow("Face Login", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return False

# ===============================
# 🚀 START SYSTEM (FACE LOGIN FIRST)
# ===============================
def start_jarvis():

    if not face_login():
        speak("Access denied")
        return

    load_contacts()
    speak("Jarvis ready")

    while True:
        command = listen()

        if command == "":
            continue

        if "hello" in command:
            speak("Hello")

        elif "weather" in command:
            get_weather_from_command(command)

        elif "time" in command:
            speak(datetime.datetime.now().strftime("%H:%M:%S"))

        elif "date" in command:
            speak(datetime.datetime.now().strftime("%A %d %B %Y"))

        elif "system" in command:
            system_status()

        elif "google":
            webbrowser.open("https://google.com")

        elif "youtube":
            webbrowser.open("https://youtube.com")

        elif "notepad" in command:
            speak("Opening Notepad")
            os.system("start notepad")

        elif "screenshot" in command:
            take_screenshot()

        elif "calculate" in command:
            calculate(command)

        elif "play" in command:
            play_song(command)

        elif "whatsapp" in command or "message" in command:
            send_whatsapp(command)

        elif "news" in command:
            get_news()

        elif "alarm" in command:
            set_alarm(command)

        elif "exit" in command:
            speak("Goodbye")
            break

        else:
            speak("Command not recognized")

# ▶ RUN
if __name__ == "__main__":
    start_jarvis()