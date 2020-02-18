import requests
import threading

from tkinter.ttk import Frame, Style
from tkinter import Tk, BOTH, LabelFrame, Label

from utils.time_utils import *
from utils.image_util import read_icons
from serials.serial_log import export_csv
from serials.serial_reader import SerialArduino, read_config

from serials.sensor_updates import update_hall, update_temp
from serials.sensor_updates import update_battery, update_speedometer
from serials.sensor_updates import update_speed, update_power, update_distance


URL = "https://edrmonitor.sutrithip.com/"


class EDRMonitor(Frame):
    def __init__(self, root, width, height):
        super().__init__()
        self.ori_width = 1536
        self.ori_height = 864
        self.width = width
        self.height = height

        self.hall = 0
        self.temp = 0
        self.batt_percentage = 100
        self.speedometer_percentage = 0

        self.VU = read_icons('./images/vu20/*.png', self.w(500), self.h(100))
        self.BATT = read_icons('./images/battery/*.png', self.w(150), self.h(100))
        self.LOGO = read_icons('./images/logo/*.png', self.w(200), self.h(200))
        self.HALL = read_icons('./images/hall/*.png', self.w(150), self.h(150))
        self.TEMP = read_icons('./images/temp/*.png', self.w(150), self.h(150))

        self.init_datetime = to_datetime_format(get_datetime_split())
        self.total_power = 0
        self.total_distance = 0
        self.records = []

        self.root = root
        self.initUI()
        self.update_time()

        # self.update_sensor_rest()
        self.init_connection()

    def init_connection(self):
        port, columns, baud_rate = read_config("./config.json")
        self.ser = SerialArduino(port, baud_rate, columns)
        self.ser.connect()
        self.update_sensor()

    def read_sensors(self, line):
        status = line.get('status', False)
        speed = line.get('speed', 0.)
        distance = line.get('distance', 0.)
        power = line.get('power', 0)
        return speed, status, power, distance

    def update_sensor(self):
        line = self.ser.readline()
        if line is None:
            print("[Error] Disconnected")
            self.init_datetime = to_datetime_format(get_datetime_split())
            self.total_power = 0
            self.total_distance = 0
            self.ser.connect()
            print("[Error] Reconnected!")
        elif line == {}:
            print("......")
        else:
            speed, status, power, distance = self.read_sensors(line)

            if status:
                self.records.append(line)
            else:
                if len(self.records) != 0:
                    export_csv(self.records, self.ser.csv_columns, save_path="logs")
                    self.records.clear()

            self.total_power += power
            self.total_distance += distance

            # update hall, speed, power, and distance
            update_hall(self.hall_lbl, status, self.HALL)
            update_speed(self.spd_lbl, speed)
            update_power(self.pw_lbl, self.total_power)
            update_distance(self.dist_lbl, self.total_distance)

        self.after(1, self.update_sensor)

    def update_sensor_rest(self):
        def sent_request():
            response = requests.get(URL)
            if response.status_code == 200:
                a = response.text
                print(a)

        t = threading.Thread(target=sent_request)
        t.start()
        self.after(1000, self.update_sensor_rest)

    def w(self, n):
        return int(self.width * n / self.ori_width / 1.09)

    def h(self, n):
        return int(self.height * n / self.ori_height / 1.09)

    def update_time(self):
        self.time_lbl.config(text=get_datetime())
        self.elapse_lbl.config(text=get_diff_time(self.init_datetime, to_datetime_format(get_datetime_split())))
        self.after(1000, self.update_time)

    def _init_image_label(self, parent, image):
        lbl = Label(parent, image=image, borderwidth=0)
        lbl.image = image
        return lbl

    def _init_text_label(self, parent, text, font_size, fg='white'):
        lbl = Label(parent, text=text, bg="#212121", fg=fg)
        lbl.config(font=("fangsongti", font_size))
        return lbl

    def initUI(self):
        self.master.title("Absolute positioning")
        self.pack(fill=BOTH, expand=1)
        Style().configure("TFrame", background="#212121")

        vu_labelframe = LabelFrame(self, bg="#212121", borderwidth=0)
        vu_labelframe.pack(side="left", anchor='w', fill='y')
        self._init_image_label(vu_labelframe, self.LOGO['edr']).pack(anchor="n")
        self.time_lbl = self._init_text_label(vu_labelframe, get_datetime(), self.h(45))
        self.time_lbl.pack(side='top')
        self.dist_lbl = self._init_text_label(vu_labelframe, "{:5.2f} KM".format(self.total_distance), self.h(85))
        self.dist_lbl.pack(side='bottom', anchor="s")
        self.pw_lbl = self._init_text_label(vu_labelframe, "{:04d} KW".format(self.total_power), self.h(75))
        self.pw_lbl.pack(side='bottom', anchor="s", pady=self.h(50))

        spd_labelframe = LabelFrame(self, borderwidth=0, bg="#212121")
        spd_labelframe.pack(side='left', fill='y')
        self.vu_lbl = self._init_image_label(spd_labelframe, self.VU['0'])
        self.vu_lbl.pack(anchor='n')
        self.pad_lbl = self._init_text_label(spd_labelframe, "{:>4}%".format(0), self.h(85))
        self.pad_lbl.pack(anchor='n')
        self.spd_lbl = self._init_text_label(spd_labelframe, "{:4.2f}".format(0), self.h(200), fg="#65dba8")
        self.spd_lbl.pack(side='top')
        self._init_text_label(spd_labelframe, "Km/hr", self.h(64), fg="#65dba8").pack(side='top')

        sensor_labelframe = LabelFrame(spd_labelframe, borderwidth=0, bg="#212121")
        sensor_labelframe.pack(side='bottom', padx=self.h(150))
        self.hall_lbl = self._init_image_label(sensor_labelframe, self.HALL['0'])
        self.hall_lbl.pack(side="left")
        self.temp_lbl = self._init_image_label(sensor_labelframe, self.TEMP[str('0')])
        self.temp_lbl.pack(side="left")


        right_labelframe = LabelFrame(self, bg="#212121", borderwidth=0)
        right_labelframe.pack(side='left', fill='y')
        batt_labelframe = LabelFrame(right_labelframe, bg="#212121", borderwidth=0)
        batt_labelframe.pack(side="top", anchor='n')
        batt_per = self.batt_percentage // 25 * 25
        self.battery_img = self._init_image_label(batt_labelframe, self.BATT[str(batt_per)])
        self.battery_img.pack(side='right', anchor='e')
        self.battery_lbl = self._init_text_label(batt_labelframe, "{:>4}%".format(self.batt_percentage), self.h(65))
        self.battery_lbl.pack(side='top', anchor='e', padx=(0, self.h(50)))
        self.elapse_lbl = self._init_text_label(right_labelframe, self.init_datetime, self.h(80))
        self.elapse_lbl.pack(side='bottom')


if __name__ == '__main__':
    # init root for display
    root = Tk()
    root.wm_attributes('-fullscreen', 'true')

    # get dimension (width, height) to make it dynamically - resizing.
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    print("width:", width, ", height:", height)

    # init the monitor from root.
    app = EDRMonitor(root, width, height)
    root.mainloop()
