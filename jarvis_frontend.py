# ===============================
# JARVIS FRONTEND WITH FACE LOGIN + IRON MAN UI 🔥
# ===============================

import customtkinter as ctk
import threading
import webbrowser
import datetime
import re
import math

# ✅ IMPORT BACKEND FUNCTIONS
from jarvis_backend import (
    speak, listen, get_weather_from_command, take_screenshot,
    calculate, play_song, send_whatsapp, system_status, get_news,
    set_alarm, face_login, load_contacts
)

# ===============================
# 🔐 FACE LOGIN FIRST
# ===============================

def start_system():

    if not face_login():
        speak("Access Denied")
        return

    load_contacts()
    speak("Welcome Reshma, Jarvis is ready")

    launch_gui()


# ===============================
# GUI FUNCTION
# ===============================

def launch_gui():

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.geometry("1100x700")
    app.title("JARVIS - IRON MAN UI")

    # HEADER
    header = ctk.CTkLabel(app, text="🤖 JARVIS AI SYSTEM",
                          font=("Arial", 34, "bold"))
    header.pack(pady=20)

    # STATUS
    status = ctk.CTkLabel(app, text="Status: Ready",
                          font=("Consolas", 18))
    status.pack(pady=10)

    def update_status(text):
        status.configure(text=f"Status: {text}")

    # ================= IRON MAN ANIMATION =================
    canvas = ctk.CTkCanvas(app, width=300, height=300, bg="black", highlightthickness=0)
    canvas.pack(pady=20)

    angle = 0
    pulse = 0
    growing = True

    def animate():
        nonlocal angle, pulse, growing
        canvas.delete("all")

        x, y = 150, 150

        # 🔵 CENTER PULSE
        if growing:
            pulse += 1
            if pulse > 20:
                growing = False
        else:
            pulse -= 1
            if pulse < 5:
                growing = True

        canvas.create_oval(
            x-20-pulse, y-20-pulse,
            x+20+pulse, y+20+pulse,
            outline="cyan", width=2
        )

        # 🌀 OUTER RING
        for i in range(8):
            start = angle + i * 45
            canvas.create_arc(
                x-100, y-100, x+100, y+100,
                start=start, extent=25,
                style="arc",
                outline="cyan",
                width=3
            )

        # 🔷 INNER RING
        for i in range(6):
            start = -angle + i * 60
            canvas.create_arc(
                x-70, y-70, x+70, y+70,
                start=start, extent=20,
                style="arc",
                outline="blue",
                width=2
            )

        # ✨ SCANNING LINE
        canvas.create_line(
            x, y,
            x + 100 * math.cos(math.radians(angle)),
            y + 100 * math.sin(math.radians(angle)),
            fill="cyan",
            width=2
        )

        angle += 4
        app.after(40, animate)

    animate()

    # THREAD
    def run_thread(func, *args):
        threading.Thread(target=func, args=args).start()

    # VOICE
    def voice():
        update_status("Listening...")
        cmd = listen()

        if cmd == "":
            update_status("No command")
            return

        update_status(cmd)

        if "weather" in cmd:
            run_thread(get_weather_from_command, cmd)

        elif "time" in cmd:
            speak(datetime.datetime.now().strftime("%H:%M:%S"))

        elif "date" in cmd:
            speak(datetime.datetime.now().strftime("%A %d %B %Y"))

        elif "system" in cmd:
            run_thread(system_status)

        elif "google" in cmd:
            webbrowser.open("https://google.com")

        elif "youtube" in cmd:
            webbrowser.open("https://youtube.com")

        elif "screenshot" in cmd:
            run_thread(take_screenshot)

        elif "calculate" in cmd:
            run_thread(calculate, cmd)

        elif "play" in cmd:
            run_thread(play_song, cmd)

        elif "whatsapp" in cmd:
            run_thread(send_whatsapp, cmd)

        elif "news" in cmd:
            run_thread(get_news)

        elif "alarm" in cmd:
            run_thread(set_alarm, cmd)

        elif "exit" in cmd:
            speak("Goodbye")
            app.destroy()

        else:
            speak("Command not recognized")

        update_status("Done")

    # FRAME
    frame = ctk.CTkFrame(app)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # BUTTONS
    buttons = [
        ("🎤 Voice", lambda: run_thread(voice)),
        ("🌦 Weather", lambda: run_thread(get_weather_from_command, "weather in delhi")),
        ("📰 News", lambda: run_thread(get_news)),
        ("📸 Screenshot", lambda: run_thread(take_screenshot)),
        ("🧮 Calc", lambda: run_thread(calculate, "calculate 5+5")),
        ("🎵 Music", lambda: run_thread(play_song, "play song")),
        ("🌐 Google", lambda: webbrowser.open("https://google.com")),
        ("▶️ YouTube", lambda: webbrowser.open("https://youtube.com")),
        ("💻 System", lambda: run_thread(system_status)),
        ("❌ Exit", app.destroy)
    ]

    row = 0
    col = 0

    for text, cmd in buttons:
        ctk.CTkButton(frame, text=text, command=cmd,
                      height=50).grid(row=row, column=col, padx=10, pady=10)

        col += 1
        if col == 3:
            col = 0
            row += 1

    app.mainloop()


# ===============================
# ▶ RUN PROGRAM
# ===============================
if __name__ == "__main__":
    start_system()