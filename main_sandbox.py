import time
import json
import threading
from tkinter import *
from utils.time_utils import *
from serial import Serial


def get_time():
    """get a string of time (Hour:Minute:Seconds)"""
    return to_time_format(get_datetime_split())


class Q:
    def __init__(self, maxsize=10):
        self.q = []
        self.maxsize = maxsize

    def enqueue(self, val):
        self.q.append(val)
        if len(self.q) > self.maxsize:
            self.q.pop(0)

    def dequeue(self):
        if len(self.q) == 0:
            raise IndexError("Queue is empty")
        return self.q.pop(0)

    def peek(self):
        if len(self.q) == 0:
            raise IndexError("Queue is empty")
        return self.q[0]

    @property
    def len(self):
        return len(self.q)

    def tolist(self):
        return self.q


class RunL1(threading.Thread):
    def __init__(self, _stop_event):
        self.time = get_time()
        self.lock = threading.Lock()
        self.stop_event = _stop_event
        threading.Thread.__init__(self)

    def run(self):
        while not self.stop_event.is_set():
            with self.lock:
                self.time = get_time()
        print("\n******************************* RUN_L1 ended *******************************")


class RunSer(threading.Thread):
    def __init__(self, _stop_event, port, baud_rate=9600, maxsize=5):
        self.q = Q(maxsize=maxsize)
        self.time = 0
        self.port = port
        self.baud_rate = baud_rate
        self.ser = self._init_connection()
        self.lock = threading.Lock()
        self.stop_event = _stop_event
        threading.Thread.__init__(self)

    def _init_connection(self):
        return Serial(self.port, self.baud_rate)

    def _extract(self):
        try:
            line = self.ser.readline()
            return line.decode().rstrip()
        except (AttributeError, UnicodeDecodeError):
            return "{}"

    def run(self):
        while not self.stop_event.is_set():
            with self.lock:
                start = time.time()
                try:
                    line = self._extract()
                    line = json.loads(line)
                except json.decoder.JSONDecodeError:
                    line = {}
                self.q.enqueue(line)
                self.time = time.time() - start
        print("\n******************************* RUN_SER ended *******************************")


class Main:
    def __init__(self):
        # init threads
        self.run_l2 = RunSer(stop_event, port="COM7", baud_rate=9600, maxsize=10)
        self.run_l2.start()

        print("Booting up...")
        time.sleep(1)

        # the GUI main object
        self.root = Tk()

        # Frames to display data
        self.l1 = Label(master=self.root, text=f"Time: {get_time()}")
        self.l2_1 = Label(master=self.root, text=f"Pedal: {0}%")
        self.l2_2 = Label(master=self.root, text=f"Speed: {0}")
        self.l3 = Label(master=self.root, text=f"GPS: {0}")
        self.l1.pack()
        self.l2_1.pack()
        self.l2_2.pack()
        self.l3.pack()

        # update every
        self.update_l1()
        self.update_l2()
        self.update_l3()

    def update_l1(self):
        self.l1.config(text=f"Time: {get_time()}")
        self.root.after(960, self.update_l1)

    def update_l2(self):
        if self.run_l2.q.len != 0:
            q = self.run_l2.q.dequeue()
            t = self.run_l2.time

            self.l2_1.config(text=f"Pedal: {q.get('pedal', 0)}%")
            self.l2_2.config(text=f"Speed: {q.get('speed', 0.00)}, {t:.2f}")

        self.root.after(20, self.update_l2)

    def update_l3(self):
        self.root.after(100, self.update_l3)


if __name__ == '__main__':
    stop_event = threading.Event()
    main = Main()
    try:
        main.root.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
