import serial
import time
import numpy as np

# Define the serial port and baud rate
serial_port = '/dev/cu.SLAB_USBtoUART'  # Replace with the appropriate serial port
baud_rate = 115200

sample_rate = 20 # Hz
time_interval = 100000

# Create a serial object
ser = serial.Serial(serial_port, baud_rate)

saved_data = []

# Read data from the serial channel
start_time = time.time()
while time.time() - start_time < time_interval:
    if ser.in_waiting > 0:
        data = ser.readline().decode().rstrip()
        data = data.split(',')
        data = data[-1]
        data = np.array(data)
        data = data.astype(np.float32)
        print(data)
        saved_data.append(data)

# saved_data = np.array(saved_data)
# print(saved_data)
# print(saved_data.shape)


