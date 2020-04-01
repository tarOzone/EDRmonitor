import time
import threading
from tkinter import *
from EDRmonitor.utils.time_utils import *

from EDRmonitor.serial.run_serial import RunSer


def get_time():
    """get a string of time (Hour:Minute:Seconds)"""
    return to_time_format(get_datetime_split())


class Main:
    def __init__(self):
        # init threads
        self.run_l2 = RunSer(stop_event, port="COM7", baud_rate=9600)
        self.run_l2.start()
        self.run_l3 = RunSer(stop_event, port="COM14", baud_rate=9600)
        self.run_l3.start()

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
        self.update_l1()    # Single thread
        self.update_l2()    # Serial
        self.update_l3()    # Serial

    def update_l1(self):
        self.l1.config(text=f"Time: {get_time()}")
        self.root.after(960, self.update_l1)

    def update_l2(self):
        q = self.run_l2.line
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
        main.root.quit()
    finally:
        stop_event.set()

    # import os
    # import csv
    # from EDRmonitor.exports import exporter
    #
    # serial_list = [
    #     {
    #         'status': True, 'mode': 1, 'pedal': 1, 'temp': 1, 'elapsed_time': 9999,
    #         'latitude': 1, 'longitude': 2, 'altitude': 3, 'speed': 4, 'distance': 5
    #     }
    # ]
    #
    # dt = get_datetime(datetime_sep="_", date_sep="-", time_sep="-")
    # csv_filename = os.path.join("logs", f"{dt}.csv")
    # f = open(csv_filename, 'w', newline='')
    #
    # writer = csv.DictWriter(f, fieldnames=exporter.columns)
    # writer.writeheader()
    # # offset = serial_list[0].copy()    # unused
    # for data in serial_list:
    #     data.pop('status', None)
    #     writer.writerow(data)
    # f.close()
