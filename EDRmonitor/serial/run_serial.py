import time
import json
import threading

from serial import Serial
from EDRmonitor.queue import queue
from serial.serialutil import SerialException


err_return = {
    'status': False, 'elapsed_time': '???', 'mode': '???', 'pedal': 50,
    'temp': 1, 'latitude': '???', 'longitude': '???',
    'altitude': '???', 'speed': 0., 'distance': 0.
}


class RunSer(threading.Thread):

    def __init__(self, _stop_event, port, baud_rate=9600, name="", ):
        self.line = {}
        self.time = 0
        self.port = port
        self.baud_rate = baud_rate
        self.ser_name = name if name else f"Serial_[{self.port}]"

        # Serial connection
        # self.ser = self._init_connection()

        self.lock = threading.Lock()
        self.stop_event = _stop_event
        threading.Thread.__init__(self)

    def _init_connection(self):
        try:
            return Serial(self.port, self.baud_rate)
        except SerialException:
            raise SerialException(f"{self.port} not found!")

    def _extract(self):
        try:
            line = self.ser.readline()
            line = line.decode().rstrip()
            return json.loads(line)
        except (AttributeError, UnicodeDecodeError, json.decoder.JSONDecodeError):
            return err_return

    def run(self):
        while not self.stop_event.is_set():
            with self.lock:
                start = time.time()
                self.line = self._extract()
                self.time = time.time() - start
        print(f"\n******************************* {self.ser_name} ended *******************************")


class RunSerQueue(threading.Thread):

    def __init__(self, _stop_event, port, baud_rate=9600, maxsize=5, name=""):
        self.q = queue.Q(maxsize=maxsize)
        self.time = 0
        self.port = port
        self.baud_rate = baud_rate
        self.ser_name = name if name else f"Serial_[{self.port}]"

        # Serial connection
        self.ser = self._init_connection()

        self.lock = threading.Lock()
        self.stop_event = _stop_event
        threading.Thread.__init__(self)

    def _init_connection(self):
        try:
            return Serial(self.port, self.baud_rate)
        except SerialException:
            raise SerialException(f"{self.port} not found!")

    def _extract(self):
        try:
            line = self.ser.readline()
            line = line.decode().rstrip()
            return json.loads(line)
        except (AttributeError, UnicodeDecodeError, json.decoder.JSONDecodeError):
            return {}

    def run(self):
        while not self.stop_event.is_set():
            with self.lock:
                start = time.time()
                line = self._extract()
                self.q.enqueue(line)
                self.time = time.time() - start
        print(f"\n******************************* {self.ser_name} ended *******************************")