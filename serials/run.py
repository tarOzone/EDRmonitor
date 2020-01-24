from time import sleep
from datetime import datetime

from tkinter import Tk, BOTH, LabelFrame, Label
from tkinter.ttk import Frame, Style

from image_util import read_icons


class Example(Frame):

    def __init__(self, root, width, height):
        super().__init__()

        self.pedal = 0
        self.hall = 0
        self.temp = 1
        self.batt_percentage = 100
        self.speed = 0
        self.power = 0
        self.count = 0
        self.distance = 0

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
        d = 1
        if self.pedal < 100:
            self.pedal += d
            self.pedal = min(100, self.pedal)
        for i in range(d):
            val, rem = divmod(self.pedal, 10)
            img = self.VU[str((val * 10) + (rem // 5 * 5))]
            self.vu_lbl.configure(image=img)
            self.vu_lbl.image = img
            self.pad_lbl.configure(text='{:>4}%'.format(self.pedal))

    def release(self, event):
        sleep(0.5)
        self.pedal = 0

        val, rem = divmod(self.pedal, 10)
        img = self.VU[str((val * 10) + (rem // 5 * 5))]
        self.vu_lbl.configure(image=img)
        self.vu_lbl.image = img
        self.pad_lbl.configure(text='{:>4}%'.format(self.pedal))

    def update_time(self):
        _time = datetime.now().strftime("%d/%m/%Y\n%H:%M:%S")
        self.time_lbl.configure(text=_time)
        self.count += 1
        minutes, seconds = divmod(divmod(self.count, 3600)[1], 60)
        _elapse_time = "{:02d}:{:02d}".format(int(minutes), int(seconds))
        self.elapse_lbl.config(text=_elapse_time)
        self.after(1000, self.update_time)

    def initUI(self):
        self.master.title("Absolute positioning")
        self.pack(fill=BOTH, expand=1)
        Style().configure("TFrame", background="#212121")

        vu_labelframe = LabelFrame(self, bg="#212121", borderwidth=0)
        vu_labelframe.pack(side="left", anchor='w', fill='y')

        img_logo = self.LOGO['edr']
        edr_lbl = Label(vu_labelframe, image=img_logo, borderwidth=0)
        edr_lbl.image = img_logo
        edr_lbl.pack(side="top")

        _time = datetime.now().strftime("%d/%m/%Y\n%H:%M:%S")
        self.time_lbl = Label(vu_labelframe, text=_time, bg="#212121", fg="white")
        self.time_lbl.config(font=("fangsongti", 44))
        self.time_lbl.pack(side='top')

        km_lbl = Label(vu_labelframe, text="KM", bg="#212121", fg="white")
        km_lbl.config(font=("Lucida Console", 45))
        km_lbl.pack(side='right', anchor="se")
        dist_lbl = Label(vu_labelframe, text="{:5.2f}".format(self.distance), bg="#212121", fg="white")
        dist_lbl.config(font=("Lucida Console", 85))
        dist_lbl.pack(side='bottom', anchor="s")

        kw_lbl = Label(vu_labelframe, text="KW", bg="#212121", fg="white")
        kw_lbl.config(font=("Lucida Console", 45))
        kw_lbl.pack(side='right', anchor="se", pady=50)
        pw_lbl = Label(vu_labelframe, text="{:04d}".format(self.power), bg="#212121", fg="white")
        pw_lbl.config(font=("Lucida Console", 75))
        pw_lbl.pack(side='bottom', anchor="s", pady=50)

        # =============================================================

        spd_labelframe = LabelFrame(self, borderwidth=0, bg="#212121")
        spd_labelframe.pack(side='left', fill='y')

        img_vu = self.VU['0']
        self.vu_lbl = Label(spd_labelframe, image=img_vu, borderwidth=0)
        self.vu_lbl.image = img_vu
        self.vu_lbl.pack(anchor='n')

        self.pad_lbl = Label(spd_labelframe, text="{:>4}%".format(0), bg="#212121", fg="white")
        self.pad_lbl.config(font=("fangsongti", 85))
        self.pad_lbl.pack(anchor='n')

        spd_lbl = Label(spd_labelframe, text="{:6.2f}".format(0), bg="#212121", fg="#65dba8")
        spd_lbl.config(font=("fangsongti", 200))
        spd_lbl.pack(side='top')
        unit_lbl = Label(spd_labelframe, text="Km/hr", bg="#212121", fg="#65dba8")
        unit_lbl.config(font=("fangsongti", 64))
        unit_lbl.pack(side='top')

        sensor_labelframe = LabelFrame(spd_labelframe, borderwidth=0, bg="#212121")
        sensor_labelframe.pack(side='bottom', padx=150)

        img_hall = self.HALL['0']
        hall_lbl = Label(sensor_labelframe, image=img_hall, borderwidth=0)
        hall_lbl.image = img_hall
        hall_lbl.pack(side="left")

        img_temp = self.TEMP[str(self.temp)]
        temp_lbl = Label(sensor_labelframe, image=img_temp, borderwidth=0)
        temp_lbl.image = img_temp
        temp_lbl.pack(side="left")

        # =============================================================

        right_labelframe = LabelFrame(self, bg="#212121", borderwidth=0)
        right_labelframe.pack(side='left', fill='y')

        batt_width, batt_height = 150, 100
        batt_labelframe = LabelFrame(right_labelframe, bg="#212121", borderwidth=0)
        batt_labelframe.pack(side="top", anchor='n', padx=batt_width // 10, pady=batt_height // 5)

        img_batt = self.BATT[str(self.batt_percentage // 10 *10)]
        battery_lbl = Label(batt_labelframe, image=img_batt, borderwidth=0)
        battery_lbl.image = img_batt
        battery_lbl.pack(side='right', anchor='e')
        batt_lbl = Label(batt_labelframe, text="{:>4}%".format(self.batt_percentage), bg="#212121", fg="white")
        batt_lbl.config(font=("fangsongti", 75))
        batt_lbl.pack(side='top', anchor='e', padx=(0, batt_width // 10))

        hours, remaining = divmod(self.count, 3600)
        minutes, seconds = divmod(remaining, 60)
        _elapse_time = "{:02d}:{:02d}".format(int(minutes), int(seconds))

        self.elapse_lbl = Label(right_labelframe, text=_elapse_time, bg="#212121", fg="white")
        self.elapse_lbl.config(font=("Lucida Console", 80))
        self.elapse_lbl.pack(side='bottom')


if __name__ == '__main__':
    root = Tk()
    root.wm_attributes('-fullscreen', 'true')

    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    print("width:", width, ", height:", height)

    app = Example(root, width, height)
    root.mainloop()

