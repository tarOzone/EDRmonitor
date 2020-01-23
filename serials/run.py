from PIL import Image, ImageTk
from tkinter import messagebox, PhotoImage
from tkinter import Tk, BOTH, Button, StringVar, RAISED, OUTSIDE, Label
from tkinter.ttk import Frame, Style


class Example(Frame):
    def __init__(self, width, height):
        super().__init__()

        self.edr_logo_size = (200, 200)
        self.start_btn_size = (200, 100)

        self.width = width
        self.height = height
        self.initUI()


    def initUI(self):

        self.master.title("Absolute positioning")
        self.pack(fill=BOTH, expand=1)

        Style().configure("TFrame", background="#212121")

        edr_logo = Image.open("edr.png")
        edr_logo = edr_logo.resize((150, 150))
        edr_logo = ImageTk.PhotoImage(edr_logo)
        edr_lbl = Label(self, image=edr_logo, borderwidth=0)
        edr_lbl.image = edr_logo
        edr_lbl.pack(side="left", anchor='n')

        batt_width, batt_heigh = 250, 125
        battery = Image.open("battery_75.png")
        battery = battery.resize((batt_width, batt_heigh))
        battery = ImageTk.PhotoImage(battery)
        battery_lbl = Label(self, image=battery, borderwidth=0)
        battery_lbl.image = battery
        battery_lbl.pack(side="right", anchor='n', padx=batt_width//10, pady=batt_heigh//10)

        batt_percent = 72
        batt_lbl = Label(self, text=f"{batt_percent}%", bg="#212121", fg="white")
        batt_lbl.config(font=("Lucida Console", 75))
        batt_lbl.pack(side="right", anchor='n', pady=batt_heigh//5)

        speed = 24.15
        spd_lbl = Label(self, text=f"{speed}", bg="#212121", fg="#30a14a")
        spd_lbl.config(font=("fangsongti", 200))
        # spd_lbl.pack(side='top', anchor='e', pady=self.height // 2.6)
        spd_lbl.pack(side='top', anchor='ne', pady=(200, 0))

        unit_lbl = Label(self, text="Km/hr", bg="#212121", fg="#30a14a")
        unit_lbl.config(font=("fangsongti", 72))
        unit_lbl.pack(side='top', anchor='e')


if __name__ == '__main__':
    root = Tk()
    root.wm_attributes('-fullscreen', 'true')

    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    print(width, height)

    app = Example(width, height)
    root.mainloop()

