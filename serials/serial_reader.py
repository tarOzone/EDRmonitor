import json
from time import sleep
from sys import platform

from serial import Serial
from serial.serialutil import SerialException, SerialTimeoutException


def read_config(config_file):
    with open(config_file, "r") as f:
        content = f.read()
    json_content = json.loads(content)

    if platform == "linux" or platform == "linux2":
        port = json_content["port_linux"]
    elif platform == "win32":
        port = json_content["port_windows"]

    columns = json_content["columns"]
    baud_rate = json_content["baud_rate"]
    return port, columns, baud_rate


class SerialArduino:

    def __init__(self, port, baud_rate, csv_columns, timeout=0.5):
        self.port = port
        self.baud_rate = baud_rate
        self.connecting = False
        self.timeout = timeout
        self.serial_lists = []
        self.csv_columns = csv_columns

        self.curr_status = False
        self.prev_status = False

    # connect to the arduino according to the port
    def connect(self):
        while not self.connect_serial():
            sleep(1)
        self.connecting = True
        print("[SUCCESS] Connection DONE!!!")

    def start(self):
        print("Started!")
        while True:
            line = self.run()
            print(line)
            if line == {}:
                break
        print("End")


    def readline(self):
        try:
            line = self.ser.readline()
            line = line.decode('utf-8').rstrip()
            line = json.loads(line)
            return line
        except json.decoder.JSONDecodeError as e:
            # print("[JSONDecodeError]", e)
            return {}
        except SerialException as e:
            # print("[SerialException]", e)
            return None

    def connect_serial(self):
        try:
            self.ser = Serial(self.port, self.baud_rate, timeout=self.timeout)
            return True
        except SerialException:
            return False

    def close(self):
        try:
            print("CLOSING...")
            self.ser.close()
            self.connecting = False
        except AttributeError:
            pass
        

if __name__ == "__main__":
    port, columns, baud_rate = read_config("config.json")
    ser = SerialArduino(port, baud_rate, columns, 5)
    ser.connect()
    while True:
        print("================================")
        ser.start()
