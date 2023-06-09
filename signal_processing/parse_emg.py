import serial


PORT = "/dev/tty.usbserial-110" 
BAUDRATE = 9600 

ser = serial.Serial(PORT, BAUDRATE)

try:
    while True:
        raw_data = ser.readline()
        data_str = raw_data.decode().strip()

        if data_str != "0":
            print(data_str)
except Exception as e:
    print("An exception occurred:", str(e))
    print("Closing serial port...")
    ser.close()


