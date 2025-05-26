import serial
import time
import pygame
import sys
import os

# === CONFIGURATION ===
MUSIC_FOLDER = r'E:\SFSU\Sem-2\NMI\Term Project\Songs'  # Folder containing your songs
ARDUINO_PORT = 'COM3'
BAUD_RATE = 9600
SERIAL_TIMEOUT = 2

EMG_CLENCH_THRESHOLD = 600  # Sensor value threshold for detecting a clench
CLENCH_COOLDOWN = 0.5   # Minimum time between clenches (in seconds)
DOUBLE_CLENCH_WINDOW = 2.0  # Max time allowed between two clenches (in seconds)

# === INIT FUNCTIONS ===
def load_playlist(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path)
            if f.lower().endswith(('.mp3', '.wav'))]

def init_music_player():
    pygame.mixer.init()

def play_track(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    print(f"🎵 Now playing: {os.path.basename(file_path)}")

def init_serial_connection(port, baud_rate, timeout=1):
    try:
        print(f"Connecting to serial port '{port}'...")
        ser = serial.Serial(port, baud_rate, timeout=timeout)
        print("✅ Serial connection established.")
        return ser
    except serial.SerialException as e:
        sys.exit(f"❌ Serial connection error: {e}")

def read_sensor_value(ser):
    try:
        line = ser.readline().decode('utf-8').strip()
        return int(line) if line.isdigit() else None
    except Exception:
        return None

# === MAIN LOOP ===
def main():
    init_music_player()
    playlist = load_playlist(MUSIC_FOLDER)
    if not playlist:
        sys.exit("❌ No music files found in the folder.")
    
    current_track = 0
    play_track(playlist[current_track])
    is_playing = True

    ser = init_serial_connection(ARDUINO_PORT, BAUD_RATE, SERIAL_TIMEOUT)

    last_clench_time = 0
    clench_count = 0

    try:
        while True:
            sensor_value = read_sensor_value(ser)
            if sensor_value is None:
                continue

            print(f"{time.strftime('%H:%M:%S')} - EMG Value: {sensor_value}")

            current_time = time.time()

            if sensor_value > EMG_CLENCH_THRESHOLD:
                # Avoid multiple detections for one clench
                if current_time - last_clench_time > CLENCH_COOLDOWN:
                    clench_count += 1
                    print(f"⚡ Clench detected (#{clench_count})")
                    if clench_count == 2:
                        if current_time - last_clench_time <= DOUBLE_CLENCH_WINDOW:
                            # Double clench: skip to next track
                            current_track = (current_track + 1) % len(playlist)
                            play_track(playlist[current_track])
                            is_playing = True
                            print("⏭️ Double clench: Skipped to next track")
                        clench_count = 0  # Reset after double clench
                    else:
                        last_clench_time = current_time

            else:
                # Reset if clench is too slow to count as double
                if current_time - last_clench_time > DOUBLE_CLENCH_WINDOW:
                    if clench_count == 1:
                        # Single clench: toggle play/pause
                        if is_playing:
                            pygame.mixer.music.pause()
                            print("⏸️ Music paused")
                        else:
                            pygame.mixer.music.unpause()
                            print("▶️ Music resumed")
                        is_playing = not is_playing
                    clench_count = 0

            # Optional: auto next if track finishes
            if not pygame.mixer.music.get_busy() and is_playing:
                current_track = (current_track + 1) % len(playlist)
                play_track(playlist[current_track])

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("👋 Interrupted by user.")
    finally:
        pygame.mixer.music.stop()
        ser.close()
        print("🛑 Music stopped and serial port closed.")

if __name__ == '__main__':
    main()
