import serial
import tkinter

# Global variable for serial connection
serial_conn = None


# Serial communication class
class SerialComm:
    def __init__(self, root):
        self.root = root
        self.serial_conn = None
        self.sensor_values = [tkinter.StringVar(value="0") for _ in range(5)]
        self.connect_serial()

    def connect_serial(self):
        try:
            self.serial_conn = serial.Serial('COM5',
                                             9600)  # Adjust 'COM5' to match the port your Arduino is connected to
            self.read_data()
        except serial.SerialException as e:
            print("Error:", e)

    def read_data(self):
        try:
            line = self.serial_conn.readline().decode().strip()
            if line:
                values = line.split(",")  # Remove the last element (empty string)
                if len(values) == 5:  # Ensure all variables are received
                    for i, value in enumerate(values):
                        self.sensor_values[i].set(value)
                else:
                    print("Incomplete data received")
            self.root.after(100, self.read_data)  # Schedule next read after 100ms
        except UnicodeDecodeError:
            print("Error decoding data, skipping line.")
            self.read_data()
