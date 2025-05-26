import serial
import time

ARDUINO_PORT = 'COM3'
BAUD_RATE = 9600
DURATION = 10  # seconds to log

def read_sensor_value(ser):
    try:
        line = ser.readline().decode('utf-8').strip()
        return int(line) if line.isdigit() else None
    except:
        return None

def main():
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=2)
    print("Logging EMG values... Relax for 5s, then clench for 5s.")
    values = []
    start_time = time.time()

    while time.time() - start_time < DURATION:
        val = read_sensor_value(ser)
        if val is not None:
            print(val)
            values.append(val)
        time.sleep(0.05)

    ser.close()
    print("\n=== STATS ===")
    print(f"Min: {min(values)}")
    print(f"Max: {max(values)}")
    print(f"Average: {sum(values) / len(values):.2f}")
    print("Copy these numbers and send them to me!")

if __name__ == '__main__':
    main()

