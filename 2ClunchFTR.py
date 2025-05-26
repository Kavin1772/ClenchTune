from collections import deque
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

PAUSE_RANGE = (300, 500)
SKIP_RANGE = (260, 480)
ACTION_COOLDOWN = 1.5
BUFFER_SIZE = 5  # For moving average

# === INIT ===
def load_playlist(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path)
            if f.lower().endswith(('.mp3', '.wav'))]

def init_music_player():
    pygame.mixer.init()

def play_track(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    print(f"🎵 Now playing: {os.path.basename(file_path)}")

def init_serial(port):
    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=SERIAL_TIMEOUT)
        print(f"✅ Connected to {port}")
        return ser
    except serial.SerialException as e:
        sys.exit(f"❌ Failed to connect to {port}: {e}")

def read_dual_emg(ser):
    try:
        line = ser.readline().decode('utf-8').strip()
        if ',' in line:
            a0, a1 = line.split(',')
            return int(a0), int(a1)
    except:
        pass
    return None, None

def moving_average(buffer, new_val):
    buffer.append(new_val)
    if len(buffer) > BUFFER_SIZE:
        buffer.popleft()
    return sum(buffer) / len(buffer)

# === MAIN LOOP ===
def main():
    playlist = load_playlist(MUSIC_FOLDER)
    if not playlist:
        sys.exit("❌ No music files found.")

    init_music_player()
    current_track = 0
    play_track(playlist[current_track])
    is_playing = True

    ser = init_serial(ARDUINO_PORT)
    last_pause_time = 0
    last_skip_time = 0

    a0_buffer = deque()
    a1_buffer = deque()

    try:
        while True:
            current_time = time.time()
            raw_a0, raw_a1 = read_dual_emg(ser)

            if raw_a0 is None or raw_a1 is None:
                continue

            avg_a0 = moving_average(a0_buffer, raw_a0)
            avg_a1 = moving_average(a1_buffer, raw_a1)

            print(f"A0 (Pause): {int(avg_a0)} | A1 (Skip): {int(avg_a1)}")

            # === Pause/Play from A0
            if PAUSE_RANGE[0] <= avg_a0 <= PAUSE_RANGE[1]:
                if current_time - last_pause_time >= ACTION_COOLDOWN:
                    if is_playing:
                        pygame.mixer.music.pause()
                        print("⏸️ Paused (A0)")
                    else:
                        pygame.mixer.music.unpause()
                        print("▶️ Resumed (A0)")
                    is_playing = not is_playing
                    last_pause_time = current_time

            # === Skip from A1
            if SKIP_RANGE[0] <= avg_a1 <= SKIP_RANGE[1]:
                if current_time - last_skip_time >= ACTION_COOLDOWN:
                    current_track = (current_track + 1) % len(playlist)
                    play_track(playlist[current_track])
                    is_playing = True
                    print("⏭️ Skipped (A1)")
                    last_skip_time = current_time

            # Auto-next track
            if not pygame.mixer.music.get_busy() and is_playing:
                current_track = (current_track + 1) % len(playlist)
                play_track(playlist[current_track])

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("👋 Exiting.")
    finally:
        pygame.mixer.music.stop()
        ser.close()
        print("🛑 Music stopped. Serial port closed.")

if __name__ == '__main__':
    main()