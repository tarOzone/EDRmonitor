import threading
from tkinter.ttk import Frame, Style
from tkinter import Tk, BOTH, LabelFrame, Label

from EDRmonitor.serial import run_serial
from EDRmonitor.utils.time_utils import *
from EDRmonitor.utils.image_util import read_icons

from EDRmonitor.serials.serial_log import export_csv
from EDRmonitor.serials.sensor_updates import update_hall, update_temp
from EDRmonitor.serials.sensor_updates import update_speedometer
from EDRmonitor.serials.sensor_updates import update_speed, update_power, update_distance


URL = "https://edrmonitor.sutrithip.com/"


class EDRMonitor(Frame):
    def __init__(self, width, height):
        super().__init__()

        # Init dimension of the display
        self.ori_width = 1536
        self.ori_height = 864
        self.width = width
        self.height = height

        # Init the initialized values
        self.hall = 0
        self.temp = 0
        self.total_power = 0
        self.total_distance = 0
        self.batt_percentage = 100
        self.speedometer_percentage = 0

        # Show images with the specific sizes
        self.VU = read_icons('data/vu20/*.png', self.w(500), self.h(100))
        self.BATT = read_icons('data/battery/*.png', self.w(150), self.h(100))
        self.LOGO = read_icons('data/logo/*.png', self.w(200), self.h(200))
        self.HALL = read_icons('data/hall/*.png', self.w(150), self.h(150))
        self.TEMP = read_icons('data/temp/*.png', self.w(150), self.h(150))

        # The processes are here
        self.init_datetime = to_datetime_format(get_datetime_split())
        self.initUI()
        self.update_time()

        # To be exported as csv
        self.records = []

        # Init serial connection
        self.init_connection()

    def init_connection(self):
        self.gps_sensor = run_serial.RunSer(stop_event, port="COM14", name="gps_sensor")
        self.gps_sensor.start()
        self.realtime_sensor = run_serial.RunSer(stop_event, port="COM7", name="realtime_sensor")
        self.realtime_sensor.start()
        self.update_sensor()

    def read_sensors(self, line):
        status = line.get('status', False)
        speed = line.get('speed', 0.)
        distance = line.get('distance', 0.)
        power = line.get('power', 0)
        temp = line.get('temp', 0)
        pedal = line.get('pedal', 0)
        return speed, status, power, distance, temp, pedal

    def update_sensor(self):
        line = self.realtime_sensor.line
        line_gps = self.gps_sensor.line
        line.update(line_gps)

        print(line)

        speed, status, power, distance, temp, pedal = self.read_sensors(line)
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
        update_temp(self.temp_lbl, temp, self.TEMP)
        update_power(self.pw_lbl, self.total_power)
        update_distance(self.dist_lbl, self.total_distance)
        update_speedometer(self.pad_lbl, self.vu_lbl, pedal, self.VU)
        self.after(20, self.update_sensor)

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
    try:
        # init root for display
        root = Tk()
        root.wm_attributes('-fullscreen', 'true')

        # get dimension (width, height) to make it dynamically - resizing.
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        print("width:", width, ", height:", height)

        # init the monitor from root.
        stop_event = threading.Event()
        app = EDRMonitor(width, height)
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()
    finally:
        stop_event.set()
