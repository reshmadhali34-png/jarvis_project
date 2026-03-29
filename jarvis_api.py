import webbrowser
import os
import datetime

from app import (
    get_weather_from_command,
    calculate,
    play_song,
    send_whatsapp,
    system_status,
    take_screenshot
)

def process_command(command):
    command = command.lower()

    try:
        if "hello" in command:
            return "Hello! I am Jarvis"

        elif "weather" in command:
            get_weather_from_command(command)
            return "Fetching weather..."

        elif "time" in command:
            return datetime.datetime.now().strftime("%H:%M:%S")

        elif "date" in command:
            return datetime.datetime.now().strftime("%A %d %B %Y")

        elif "google" in command:
            webbrowser.open("https://google.com")
            return "Opening Google"

        elif "youtube" in command:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube"

        elif "notepad" in command:
            os.system("notepad")
            return "Opening Notepad"

        elif "screenshot" in command:
            take_screenshot()
            return "Screenshot taken"

        elif "calculate" in command:
            calculate(command)
            return "Calculating..."

        elif "play" in command:
            play_song(command)
            return "Playing on YouTube"

        elif "whatsapp" in command or "message" in command:
            send_whatsapp(command)
            return "Sending message..."

        elif "news" in command:
            return "Use voice mode for news"

        elif "system" in command:
            system_status()
            return "Checking system..."

        else:
            return "Sorry, I did not understand"

    except:
        return "Error executing command"