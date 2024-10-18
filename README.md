
# Talking Clock with Alarm and Multi-Language Support

## Description
The Talking Clock project is a Python-based desktop application that visually displays the current time and date, and can also announce the time using pre-recorded audio in different languages. Users can switch between multiple languages and set alarms that trigger time announcements.

## Features
- Time and date display with automatic updates.
- Audio announcements in English, German, Chinese, and French.
- Language switching functionality.
- Alarm setting with time announcement as the reminder.
- Day and night mode toggle for visual customization.

## Dependencies
- **Python 3.x**: Ensure Python is installed on your system.
- **Tkinter**: For the GUI (included in Python by default).
- **Pygame**: For audio playback. Install using:
  ```bash
  pip install pygame
  ```

## How to Run
1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2. Navigate to the project directory:
    ```bash
    cd talking_clock
    ```
3. Install the required dependencies:
    ```bash
    pip install pygame
    ```
4. Run the application:
    ```bash
    python talking_clock.py
    ```

## Customization
- **Adding Languages**: To add a new language, create a folder in the `audio` directory for the new language and place the respective audio files for hours, minutes, and time expressions. Modify the `voice_folders` dictionary to include the new language.
