import serial
import time
import pygame
import sys
import os

# Constants
MUSIC_FOLDER = r'E:\SFSU\Sem-2\NMI\Term Project\Songs'
ARDUINO_PORT = 'COM3'
BAUD_RATE = 9600
SERIAL_TIMEOUT = 2

# Sensor value thresholds
PLAY_THRESHOLD = 600
NEXT_COMMAND = 700
PREV_COMMAND = 800

def load_playlist(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path)
            if f.lower().endswith(('.mp3', '.wav'))]

def init_music_player():
    pygame.mixer.init()

def play_track(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    print(f"Now playing: {os.path.basename(file_path)}")

def init_serial_connection(port, baud_rate, timeout=1):
    try:
        print(f"Connecting to serial port '{port}'...")
        ser = serial.Serial(port, baud_rate, timeout=timeout)
        print("Serial connection established.")
        return ser
    except serial.SerialException as e:
        sys.exit(f"Serial connection error: {e}")

def read_sensor_value(ser):
    try:
        line = ser.readline().decode('utf-8').strip()
        return int(line) if line.isdigit() else None
    except Exception:
        return None

def main():
    init_music_player()
    playlist = load_playlist(MUSIC_FOLDER)
    if not playlist:
        sys.exit("No music files found in the folder.")
    
    current_track = 0
    play_track(playlist[current_track])
    is_playing = True

    ser = init_serial_connection(ARDUINO_PORT, BAUD_RATE, SERIAL_TIMEOUT)

    try:
        while True:
            sensor_value = read_sensor_value(ser)
            if sensor_value is None:
                continue

            print(f"{time.strftime('%H:%M:%S')} - Sensor Value: {sensor_value}")

            # Pause / Play logic
            if sensor_value < PLAY_THRESHOLD:
                if not is_playing:
                    pygame.mixer.music.unpause()
                    print("Resuming music")
                    is_playing = True
            elif sensor_value >= PLAY_THRESHOLD and sensor_value < NEXT_COMMAND:
                if is_playing:
                    pygame.mixer.music.pause()
                    print("Pausing music")
                    is_playing = False

            # Skip to next track
            elif sensor_value == NEXT_COMMAND:
                current_track = (current_track + 1) % len(playlist)
                play_track(playlist[current_track])
                is_playing = True

            # Go to previous track
            elif sensor_value == PREV_COMMAND:
                current_track = (current_track - 1) % len(playlist)
                play_track(playlist[current_track])
                is_playing = True

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        pygame.mixer.music.stop()
        ser.close()
        print("Music stopped and serial port closed.")

if __name__ == '__main__':
    main()
