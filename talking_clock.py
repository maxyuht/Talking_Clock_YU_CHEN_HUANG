import tkinter as tk
from tkinter import ttk
import time
import threading
import pygame  # used for playing audio files

# Define voice folders
voice_folders = {
    'English': 'English_audio',
    'German': 'German_audio',
    'Chinese': 'Chinese_audio',
    'French': 'French_audio'
}


class TalkingClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Talking Clock with Alarm")

        # Initialize the pygame audio module
        pygame.mixer.init()

        # Current language, default is English
        self.current_language = 'English'
        self.alarm_set = False

        # Default is day mode
        self.is_night_mode = False

        # Arrange using grid layout
        self.root.grid_columnconfigure(0, weight=1)  # Center horizontally
        self.root.grid_rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8], weight=1)  # Row proportions

        # Time display label
        self.time_label = tk.Label(root, text="", font=("Helvetica", 90, "bold"))
        self.time_label.grid(row=0, column=0, pady=(20, 10))

        # Date display label
        self.date_label = tk.Label(root, text="", font=("Helvetica", 24))
        self.date_label.grid(row=1, column=0, pady=(10, 20))

        # Current language label
        self.language_label = tk.Label(root, text=f"Current Language: {self.current_language}", font=("Helvetica", 18))
        self.language_label.grid(row=2, column=0, pady=10)

        # Switch language button
        self.switch_language_button = tk.Button(root, text="Switch Language", command=self.switch_language,
                                                font=("Helvetica", 16), borderwidth=0)
        self.switch_language_button.grid(row=3, column=0, pady=10)

        # Play voice button
        self.speak_button = tk.Button(root, text="Speak Time", command=self.speak_time, font=("Helvetica", 16),
                                      borderwidth=0)
        self.speak_button.grid(row=4, column=0, pady=10)

        # Night/Day mode toggle button
        self.switch_mode_button = tk.Button(root, text="Switch to Night Mode", command=self.toggle_mode,
                                            font=("Helvetica", 16), borderwidth=0)
        self.switch_mode_button.grid(row=6, column=0, pady=10)

        # Alarm setting
        alarm_frame = tk.Frame(root)
        alarm_frame.grid(row=5, column=0, pady=20)

        # choose hour（0-23）
        self.hour_var = tk.StringVar(value="Hours")
        hours = [f"{i:02d}" for i in range(24)]  # Generate hour options from '00' to '23'
        self.hour_menu = tk.OptionMenu(alarm_frame, self.hour_var, *hours)
        self.hour_menu.config(width=5, font=("Helvetica", 16))
        self.hour_menu.grid(row=0, column=0, padx=5)

        # choose minute（00-59）
        self.minute_var = tk.StringVar(value="Minutes")
        minutes = [f"{i:02d}" for i in range(60)]  # Generate minute options from '00' to '59'
        self.minute_menu = tk.OptionMenu(alarm_frame, self.minute_var, *minutes)
        self.minute_menu.config(width=5, font=("Helvetica", 16))
        self.minute_menu.grid(row=0, column=1, padx=5)

        # Set alarm button
        self.set_alarm_button = tk.Button(alarm_frame, text="Set Alarm", command=self.set_alarm, font=("Helvetica", 16),
                                          borderwidth=0)
        self.set_alarm_button.grid(row=0, column=2, padx=10)

        # Volume slider
        volume_frame = tk.Frame(root)
        volume_frame.grid(row=7, column=0, pady=10)

        volume_label = tk.Label(volume_frame, text="Volume", font=("Helvetica", 16))
        volume_label.grid(row=0, column=0, padx=10)

        self.volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient="horizontal", command=self.adjust_volume)
        self.volume_slider.set(100)  # Set the default volume to 100%
        self.volume_slider.grid(row=0, column=1)

        # Update the displayed time
        self.update_time()

    def adjust_volume(self, val):
        """adjust volume"""
        volume = int(val) / 100  # Convert the value from 0-100 to 0.0-1.0
        pygame.mixer.music.set_volume(volume)

    def adjust_speed(self, val):
        """adjust speak rate"""
        speed = int(val) / 150  # Adjust the rate using a relative standard speed
        pygame.mixer.music.set_volume(speed)

    def switch_language(self):
        """switch languages"""
        if self.current_language == 'English':
            self.current_language = 'German'
        elif self.current_language == 'German':
            self.current_language = 'Chinese'
        elif self.current_language == 'Chinese':
            self.current_language = 'French'
        else:
            self.current_language = 'English'
        self.language_label.config(text=f"Current Language: {self.current_language}")  # Update the displayed current language

    def toggle_mode(self):
        """Switch between night and day mode"""
        if self.is_night_mode:
            self.set_day_mode()
            self.switch_mode_button.config(text="Switch to Night Mode")
        else:
            self.set_night_mode()
            self.switch_mode_button.config(text="Switch to Day Mode")
        self.is_night_mode = not self.is_night_mode

    def set_night_mode(self):
        """Set night mode colors"""
        self.root.config(bg="#2C3E50")  # dark background
        self.time_label.config(bg="#2C3E50", fg="#ECF0F1")  # white text
        self.date_label.config(bg="#2C3E50", fg="#ECF0F1")
        self.language_label.config(bg="#2C3E50", fg="#ECF0F1")

    def set_day_mode(self):
        """Set day mode colors"""
        self.root.config(bg="#ECF0F1")  # light background
        self.time_label.config(bg="#ECF0F1", fg="#2C3E50")  # dark text
        self.date_label.config(bg="#ECF0F1", fg="#2C3E50")
        self.language_label.config(bg="#ECF0F1", fg="#2C3E50")

    def play_audio(self, filename):
        """Play specified audio file"""
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    def get_time_expression_english(self):
        """Generate audio sequence for English time expression"""
        current_time = time.strftime('%I %M %p')  # Get the current time in 24-hour format
        hour, minute, period = current_time.split()
        hour = int(hour)
        minute = int(minute)

        audio_sequence = []

        # Add "it's"
        audio_sequence.append(f"{voice_folders['English']}/it's.wav")

        # Determine the minute and concatenate the corresponding audio
        if minute == 0:
            audio_sequence.append(f"{voice_folders['English']}/{hour}.wav")
            audio_sequence.append(f"{voice_folders['English']}/o'clock.wav")
        elif minute == 15:
            audio_sequence.append(f"{voice_folders['English']}/a.wav")
            audio_sequence.append(f"{voice_folders['English']}/quarter_past.wav")
            audio_sequence.append(f"{voice_folders['English']}/{hour}.wav")
        elif minute == 30:
            audio_sequence.append(f"{voice_folders['English']}/half_past.wav")
            audio_sequence.append(f"{voice_folders['English']}/{hour}.wav")
        elif minute == 45:
            next_hour = (hour % 12) + 1
            audio_sequence.append(f"{voice_folders['English']}/a.wav")
            audio_sequence.append(f"{voice_folders['English']}/quarter_to.wav")
            audio_sequence.append(f"{voice_folders['English']}/{next_hour}.wav")
        elif minute < 10:
            audio_sequence.append(f"{voice_folders['English']}/{hour}.wav")
            audio_sequence.append(f"{voice_folders['English']}/o.wav")
            audio_sequence.append(f"{voice_folders['English']}/{minute}.wav")
        else:
            audio_sequence.append(f"{voice_folders['English']}/{hour}.wav")
            audio_sequence.append(f"{voice_folders['English']}/{minute}.wav")

        # Add AM/PM
        if period == "AM":
            audio_sequence.append(f"{voice_folders['English']}/am.wav")
        else:
            audio_sequence.append(f"{voice_folders['English']}/pm.wav")

        return audio_sequence

    def get_time_expression_german(self):
        """Generate audio sequence for German time expression"""
        current_time = time.strftime('%H %M')  # Get the current time in 24-hour format
        hour, minute = map(int, current_time.split())

        audio_sequence = []

        # Add "es ist"
        audio_sequence.append(f"{voice_folders['German']}/es_ist.wav")

        # Determine the minute and concatenate the corresponding audio
        if minute == 0:
            audio_sequence.append(f"{voice_folders['German']}/{hour}.wav")
            audio_sequence.append(f"{voice_folders['German']}/uhr.wav")
        elif minute == 15:
            audio_sequence.append(f"{voice_folders['German']}/viertel_nach.wav")
            audio_sequence.append(f"{voice_folders['German']}/{hour}.wav")
        elif minute == 30:
            next_hour = (hour % 24) + 1
            audio_sequence.append(f"{voice_folders['German']}/halb.wav")
            audio_sequence.append(f"{voice_folders['German']}/{next_hour}.wav")
        elif minute == 45:
            next_hour = (hour % 24) + 1
            audio_sequence.append(f"{voice_folders['German']}/viertel_vor.wav")
            audio_sequence.append(f"{voice_folders['German']}/{next_hour}.wav")
        else:
            audio_sequence.append(f"{voice_folders['German']}/{hour}.wav")
            audio_sequence.append(f"{voice_folders['German']}/uhr.wav")
            audio_sequence.append(f"{voice_folders['German']}/{minute}.wav")

        return audio_sequence

    def get_time_expression_chinese(self):
        """Generate audio sequence for Chinese time expression"""
        current_time = time.strftime('%H %M')  # Get the current time in 24-hour format
        hour, minute = map(int, current_time.split())

        audio_sequence = []

        # Add Chinese time expression， "3点26分"  "3点整"
        audio_sequence.append(f"{voice_folders['Chinese']}/{hour}.wav")  # 小时
        audio_sequence.append(f"{voice_folders['Chinese']}/点.wav")  # "点"
        if minute == 0:
            audio_sequence.append(f"{voice_folders['Chinese']}/整.wav")  # "整"
        else:
            audio_sequence.append(f"{voice_folders['Chinese']}/{minute}.wav")  # 分钟
            audio_sequence.append(f"{voice_folders['Chinese']}/分.wav")  # "分"

        return audio_sequence

    def get_time_expression_french(self):
        """Generate audio sequence for French time expression"""
        current_time = time.strftime('%H %M')  # Get the current time in 24-hour format
        hour, minute = map(int, current_time.split())

        audio_sequence = []

        # Add "il est"
        audio_sequence.append(f"{voice_folders['French']}/il_est.wav")

        if minute == 0:
            audio_sequence.append(f"{voice_folders['French']}/{hour:02d}_heure.wav")
        # translates to "If minute == 0, directly return the audio sequence without playing the minute part
        # Handle the minutes and concatenate the corresponding audio
        if minute == 15:
            audio_sequence.append(f"{voice_folders['French']}/{hour:02d}_heure.wav")
            audio_sequence.append(f"{voice_folders['French']}/et_quart.wav")
        elif minute == 30:
            audio_sequence.append(f"{voice_folders['French']}/{hour:02d}_heure.wav")
            audio_sequence.append(f"{voice_folders['French']}/et_demie.wav")
        elif minute == 45:
            next_hour = (hour % 24) + 1
            audio_sequence.append(f"{voice_folders['French']}/{next_hour:02d}_heure.wav")
            audio_sequence.append(f"{voice_folders['French']}/moins_le_quart.wav")
        else:
            audio_sequence.append(f"{voice_folders['French']}/{hour:02d}_heure.wav")
            audio_sequence.append(f"{voice_folders['French']}/{minute}.wav")

        return audio_sequence

    def speak_time(self):
        """Play the audio segments of the current time"""
        if self.current_language == 'English':
            audio_sequence = self.get_time_expression_english()  # English version
        elif self.current_language == 'German':
            audio_sequence = self.get_time_expression_german()  # German version
        elif self.current_language == 'Chinese':
            audio_sequence = self.get_time_expression_chinese()  # Chinese version
        elif self.current_language == 'French':
            audio_sequence = self.get_time_expression_french()  # French version

        for audio_file in audio_sequence:
            self.play_audio(audio_file)  # Play each audio file in sequence

    def set_alarm(self):
        # Get the user's selected alarm time
        alarm_hour = self.hour_var.get()
        alarm_minute = self.minute_var.get()

        # Validate the alarm time format
        if alarm_hour.isdigit() and alarm_minute.isdigit():
            self.alarm_set = True
            # Start a new thread to monitor the time
            threading.Thread(target=self.monitor_alarm, args=(int(alarm_hour), int(alarm_minute)), daemon=True).start()
            print(f"Alarm set for {alarm_hour}:{alarm_minute}")
        else:
            print("Invalid time format")

    def monitor_alarm(self, alarm_hour, alarm_minute):
        # Continuously monitor the system time until the alarm time is reached
        while self.alarm_set:
            current_hour = int(time.strftime('%H'))
            current_minute = int(time.strftime('%M'))

            if current_hour == alarm_hour and current_minute == alarm_minute:
                self.speak_time()  # Play the time as an alarm reminder
                self.alarm_set = False  # Turn off the reminder
                break
            time.sleep(1)  # Check the time every 1 second

    def update_time(self):
        """Update the displayed current time"""
        current_time = time.strftime('%H:%M:%S')
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)


# Main program entry point
if __name__ == "__main__":
    root = tk.Tk()

    # Set window size and disable resizing
    app = TalkingClockApp(root)
    root.geometry("500x600")  # Set window size
    root.resizable(False, False)  # disable resizing

    root.mainloop()

