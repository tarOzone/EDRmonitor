from datetime import datetime

from PIL import Image, ImageTk
from tkinter import Tk, BOTH, LabelFrame, Label
from tkinter.ttk import Frame, Style


class Example(Frame):

    def __init__(self, width, height):
        super().__init__()
        self.edr_logo_size = (200, 200)
        self.start_btn_size = (200, 100)
        self.width = width
        self.height = height
        self.initUI()

    def read_img(self, impath, resize_width=None, resize_height=None):
        img = Image.open(impath)
        if resize_width or resize_height:
            img = img.resize((resize_width, resize_height))
        img = ImageTk.PhotoImage(img)
        return img

    def initUI(self):
        self.master.title("Absolute positioning")
        self.pack(fill=BOTH, expand=1)
        Style().configure("TFrame", background="#212121")


        vu_width, vu_height = 300, 100
        vu_labelframe = LabelFrame(self, bg="#212121", borderwidth=0)
        vu_labelframe.pack(side="left", anchor='w', fill='y')

        vu_meter = self.read_img("vu/90.png", vu_width, vu_height)
        vu_lbl = Label(vu_labelframe, image=vu_meter, borderwidth=0)
        vu_lbl.image = vu_meter
        vu_lbl.pack(anchor='nw')

        ped_percent = 90
        pad_lbl = Label(vu_labelframe, text=f"{ped_percent}%", bg="#212121", fg="white")
        pad_lbl.config(font=("fangsongti", 85))
        pad_lbl.pack(anchor='nw')

        distance = 16.50
        km_lbl = Label(vu_labelframe, text="KM", bg="#212121", fg="white")
        km_lbl.config(font=("Lucida Console", 45))
        km_lbl.pack(side='right', anchor="se")
        dist_lbl = Label(vu_labelframe, text="{:.2f}".format(distance), bg="#212121", fg="white")
        dist_lbl.config(font=("Lucida Console", 85))
        dist_lbl.pack(side='bottom', anchor="s")

        power = 655
        kw_lbl = Label(vu_labelframe, text="KW", bg="#212121", fg="white")
        kw_lbl.config(font=("Lucida Console", 45))
        kw_lbl.pack(side='right', anchor="se", pady=vu_height//2)
        pw_lbl = Label(vu_labelframe, text="{:04d}".format(power), bg="#212121", fg="white")
        pw_lbl.config(font=("Lucida Console", 75))
        pw_lbl.pack(side='bottom', anchor="s", pady=vu_height//2)

        # =============================================================

        spd_labelframe = LabelFrame(self, borderwidth=0, bg="#212121")
        spd_labelframe.pack(side='left', fill='y')

        logo_width, logo_height = 150, 150
        edr_logo = self.read_img("edr.png", logo_width, logo_height)
        edr_lbl = Label(spd_labelframe, image=edr_logo, borderwidth=0)
        edr_lbl.image = edr_logo
        edr_lbl.pack(side="top")

        _time = datetime.now().strftime("%d/%m/%Y\n%H:%M:%S")
        time_lbl = Label(spd_labelframe, text=_time, bg="#212121", fg="white")
        time_lbl.config(font=("fangsongti", 24))
        time_lbl.pack(side='top')

        speed = 24.15
        spd_lbl = Label(spd_labelframe, text=f"{speed}", bg="#212121", fg="#65dba8")
        spd_lbl.config(font=("fangsongti", 200))
        spd_lbl.pack(side='top')
        unit_lbl = Label(spd_labelframe, text="Km/hr", bg="#212121", fg="#65dba8")
        unit_lbl.config(font=("fangsongti", 64))
        unit_lbl.pack(side='top')

        icon_width, icon_height = 150, 150
        sensor_labelframe = LabelFrame(spd_labelframe, borderwidth=0, bg="#212121")
        sensor_labelframe.pack(side='bottom', padx=icon_width)

        edr_logo = self.read_img("hall_1.png", icon_width, icon_height)
        edr_lbl = Label(sensor_labelframe, image=edr_logo, borderwidth=0)
        edr_lbl.image = edr_logo
        edr_lbl.pack(side="left")

        edr_logo = self.read_img("temp_medium.png", icon_width, icon_height)
        edr_lbl = Label(sensor_labelframe, image=edr_logo, borderwidth=0)
        edr_lbl.image = edr_logo
        edr_lbl.pack(side="left")

        # =============================================================

        batt_percent = 23

        right_labelframe = LabelFrame(self, bg="#212121", borderwidth=0)
        right_labelframe.pack(side='left', fill='y')

        batt_width, batt_height = 150, 100
        batt_labelframe = LabelFrame(right_labelframe, bg="#212121", borderwidth=0)
        batt_labelframe.pack(side="top", anchor='n', padx=batt_width // 10, pady=batt_height // 5)

        battery = self.read_img("battery_25.png", batt_width, batt_height)
        battery_lbl = Label(batt_labelframe, image=battery, borderwidth=0)
        battery_lbl.image = battery
        battery_lbl.pack(side='right', anchor='e')
        batt_lbl = Label(batt_labelframe, text=f"{batt_percent}%", bg="#212121", fg="white")
        batt_lbl.config(font=("fangsongti", 75))
        batt_lbl.pack(side='top', anchor='e', padx=(0, batt_width // 10))

        power = "06:55"
        pw_lbl = Label(right_labelframe, text=power, bg="#212121", fg="white")
        pw_lbl.config(font=("Lucida Console", 80))
        pw_lbl.pack(side='bottom')


if __name__ == '__main__':
    root = Tk()
    root.wm_attributes('-fullscreen', 'true')

    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    print(width, height)

    app = Example(width, height)
    root.mainloop()

