import serial
import time
import pygame
import sys
import os

# === CONFIGURATION ===
MUSIC_FOLDER = r'E:\SFSU\Sem-2\NMI\Term Project\Songs'
ARDUINO_PORT = 'COM3'
BAUD_RATE = 9600
SERIAL_TIMEOUT = 2

CLENCH_RANGE = (280, 360)     # Valid clench range
CLENCH_WINDOW = 2.0           # Time window for double clench
ACTION_COOLDOWN = 1.0         # Cooldown to prevent bouncing

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
    except:
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

    clench_times = []
    last_action_time = 0

    try:
        while True:
            sensor_value = read_sensor_value(ser)
            if sensor_value is None:
                continue

            current_time = time.time()
            print(f"{time.strftime('%H:%M:%S')} - EMG: {sensor_value}")

            # === Ignore noise or rest ===
            if sensor_value > 600 or sensor_value < 250:
                continue

            # === Detect valid clench ===
            if CLENCH_RANGE[0] <= sensor_value <= CLENCH_RANGE[1]:
                if current_time - last_action_time < ACTION_COOLDOWN:
                    continue  # prevent spamming

                clench_times.append(current_time)
                last_action_time = current_time
                print("⚡ Clench detected")

                # Keep only recent clenches
                clench_times = [t for t in clench_times if current_time - t <= CLENCH_WINDOW]

                if len(clench_times) == 2:
                    current_track = (current_track + 1) % len(playlist)
                    play_track(playlist[current_track])
                    is_playing = True
                    print("⏭️ Double clench: Skipped track")
                    clench_times.clear()

                elif len(clench_times) == 1:
                    # Wait to see if a second clench comes in time
                    pass

            # === Timeout check for single clench ===
            if len(clench_times) == 1 and (current_time - clench_times[0] > CLENCH_WINDOW):
                if is_playing:
                    pygame.mixer.music.pause()
                    print("⏸️ Music paused (single clench)")
                else:
                    pygame.mixer.music.unpause()
                    print("▶️ Music resumed (single clench)")
                is_playing = not is_playing
                clench_times.clear()

            # === Auto-play next track if current ends ===
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
