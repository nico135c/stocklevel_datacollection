import serial
import time

class ArduinoReader:
    def __init__(self, port="/dev/ttyACM0", baud=115200):
        self.port = port
        self.baud = baud
        self.ser = None

    def start(self):
        self.ser = serial.Serial(self.port, self.baud, timeout=1)
        time.sleep(2)  # Let Arduino reset

    def stop(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def get_next(self, count):
        print(f"Reading {count} samples...\n")

        self.ser.reset_input_buffer()

        readings = []
        while len(readings) < count:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode("utf-8", errors="replace").strip()
                if line:
                    try:
                        dist = float(line)
                    except:
                        dist = 0
                    readings.append(dist)

        return readings
