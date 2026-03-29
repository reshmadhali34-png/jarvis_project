import datetime
import webbrowser
import os
import random

def process_command(command):
    command = command.lower()

    # ---------------- GREETING ----------------
    if "hi" in command or "hello" in command or "hii" in command:
        return "Hello! I am Jarvis. How can I help you?"

    # ---------------- TIME ----------------
    elif "time" in command:
        return datetime.datetime.now().strftime("%H:%M:%S")

    # ---------------- DATE ----------------
    elif "date" in command or "today" in command:
        return datetime.datetime.now().strftime("%A, %d %B %Y")

    # ---------------- OPEN NOTEPAD ----------------
    elif "notepad" in command:
        os.system("notepad")
        return "Opening Notepad"

    # ---------------- OPEN CALCULATOR ----------------
    elif "calculator" in command:
        os.system("calc")
        return "Opening Calculator"

    # ---------------- OPEN YOUTUBE ----------------
    elif "youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    # ---------------- OPEN GOOGLE ----------------
    elif "google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google"

    # ---------------- JOKE ----------------
    elif "joke" in command:
        jokes = [
            "Why programmers hate nature? It has too many bugs!",
            "I told my computer I needed a break, it said no problem—it crashed.",
            "Why do Java developers wear glasses? Because they don't see sharp!"
        ]
        return random.choice(jokes)

    # ---------------- EXIT ----------------
    elif "exit" in command:
        return "Goodbye"

    # ---------------- DEFAULT ----------------
    else:
        return "Sorry, I did not understand"