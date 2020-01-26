from time import sleep
from datetime import datetime

from tkinter import Tk, BOTH, LabelFrame, Label
from tkinter.ttk import Frame, Style

from image_util import read_icons


def get_datetime(sep="\n"):
    return datetime.now().strftime(f"%d/%m/%Y{sep}%H:%M:%S")


def to_time_format(counter):
    hour, remaining = divmod(counter, 3600)
    minutes, seconds = divmod(remaining, 60)
    _elapse_time = "{:02d}:{:02d}".format(int(minutes), int(seconds))
    return _elapse_time


class Example(Frame):

    def __init__(self, root, width, height):
        super().__init__()

        self.pedal = 0
        self.hall = 0
        self.temp = 0
        self.speed = 0
        self.power = 0
        self.count = 0
        self.distance = 0
        self.batt_percentage = 29

        self.VU = read_icons('images/vu20/*.png', 500, 100)
        self.BATT = read_icons('images/battery/*.png', 150, 100)
        self.LOGO = read_icons('images/logo/*.png', 200, 200)
        self.HALL = read_icons('images/hall/*.png', 150, 150)
        self.TEMP = read_icons('images/temp/*.png', 150, 150)

        self.root = root
        self.width = width
        self.height = height
        self.initUI()

        self.root.bind('<KeyPress>', self.press)
        self.root.bind('<KeyRelease>', self.release)
        self.update_time()

    def press(self, event):
        self.pedal += 1
        self.pedal = min(100, max(0, self.pedal))
        self.update_vu(self.pedal)

    def release(self, event):
        sleep(0.5)
        self.pedal = 0
        self.update_vu(0)

    def map_vu_meter(self, speed):
        large_div, small_div = 10, 5
        val, rem = divmod(speed, large_div)
        return (val * large_div) + (rem // small_div * small_div)

    def update_vu(self, speed):
        vu_val = self.map_vu_meter(speed)
        vu_img = self.VU[str(vu_val)]
        self.vu_lbl.configure(image=vu_img)
        self.vu_lbl.image = vu_img
        self.pad_lbl.configure(text='{:>4}%'.format(speed))

    def map_bett_percent(self, percent):
        val, rem = divmod(percent, 25)
        offset = 1 if rem != 0 else 0
        return (val + offset) * 25

    def update_batt(self, percent):
        batt_val = self.map_bett_percent(percent)
        batt_img = self.BATT[str(batt_val)]
        self.battery_img.configure(image=batt_img)
        self.battery_img.image = batt_img
        self.battery_lbl.configure(text="{:>4}%".format(percent))

    def update_time(self):
        self.count += 1
        self.time_lbl.configure(text=get_datetime())
        self.elapse_lbl.config(text=to_time_format(self.count))
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

        self.time_lbl = self._init_text_label(vu_labelframe, get_datetime(), 45)
        self.time_lbl.pack(side='top')

        self.dist_lbl = self._init_text_label(vu_labelframe, "{:5.2f} KM".format(self.distance), 85)
        self.dist_lbl.pack(side='bottom', anchor="s")

        self.pw_lbl = self._init_text_label(vu_labelframe, "{:04d} KW".format(self.power), 75)
        self.pw_lbl.pack(side='bottom', anchor="s", pady=50)

        # =============================================================

        spd_labelframe = LabelFrame(self, borderwidth=0, bg="#212121")
        spd_labelframe.pack(side='left', fill='y')

        self.vu_lbl = self._init_image_label(spd_labelframe, self.VU['0'])
        self.vu_lbl.pack(anchor='n')
        self.pad_lbl = self._init_text_label(spd_labelframe, "{:>4}%".format(0), 85)
        self.pad_lbl.pack(anchor='n')

        self.spd_lbl = self._init_text_label(spd_labelframe, "{:4.2f}".format(0), 200, fg="#65dba8")
        self.spd_lbl.pack(side='top')
        self._init_text_label(spd_labelframe, "Km/hr", 64, fg="#65dba8").pack(side='top')

        sensor_labelframe = LabelFrame(spd_labelframe, borderwidth=0, bg="#212121")
        sensor_labelframe.pack(side='bottom', padx=150)

        self.hall_lbl = self._init_image_label(sensor_labelframe, self.HALL['0'])
        self.hall_lbl.pack(side="left")

        self.temp_lbl = self._init_image_label(sensor_labelframe, self.TEMP[str('0')])
        self.temp_lbl.pack(side="left")

        # =============================================================

        right_labelframe = LabelFrame(self, bg="#212121", borderwidth=0)
        right_labelframe.pack(side='left', fill='y')

        batt_labelframe = LabelFrame(right_labelframe, bg="#212121", borderwidth=0)
        batt_labelframe.pack(side="top", anchor='n')

        batt_per = self.batt_percentage // 25 * 25
        self.battery_img = self._init_image_label(batt_labelframe, self.BATT[str(batt_per)])
        self.battery_img.pack(side='right', anchor='e')

        self.battery_lbl = self._init_text_label(batt_labelframe, "{:>4}%".format(self.batt_percentage), 65)
        self.battery_lbl.pack(side='top', anchor='e', padx=(0, 50))

        self.elapse_lbl = self._init_text_label(right_labelframe, to_time_format(self.count), 80)
        self.elapse_lbl.pack(side='bottom')


if __name__ == '__main__':
    root = Tk()
    root.wm_attributes('-fullscreen', 'true')

    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    print("width:", width, ", height:", height)

    app = Example(root, width, height)
    root.mainloop()
