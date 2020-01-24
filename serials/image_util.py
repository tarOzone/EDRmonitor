import os
from glob import glob
from PIL import Image, ImageTk


def _read_img(impath, resize_width=None, resize_height=None):
    img = Image.open(impath)
    if resize_width or resize_height:
        img = img.resize((resize_width, resize_height))
    img = ImageTk.PhotoImage(img)
    return img


def read_icons(icon_path, width, height):
    icons_dict = {}
    for img in glob(icon_path):
        percent = os.path.splitext(os.path.basename(img))[0]
        icons_dict[int(percent)] = _read_img(img, width, height)
    return icons_dict
