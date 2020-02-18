

def _map_0_to_100(val):
    val = min(val, 100)
    val = max(val, 0)
    return val


def _update_text_label(txt_lbl, val, name):
    if name == 'speed':
        val = f"{val:4.2f}"
    elif name == 'power':
        val = f"{val:04d} KW"
    elif name == 'distance':
        val = f"{val:5.2f} KM"
    elif name == 'battery':
        val = f"{val:>4}%"
    elif name == 'speedometer':
        val = f"{val:>4}%"
    else:
        return
    txt_lbl.config(text=val)


def _update_img(img_lbl, img):
    img_lbl.configure(image=img)
    img_lbl.image = img


def update_speed(spd_lbl, spd_val):
    _update_text_label(spd_lbl, spd_val, 'speed')


def update_power(pw_lbl, pw_val):
    _update_text_label(pw_lbl, pw_val, 'power')


def update_distance(dist_lbl, dist_val):
    _update_text_label(dist_lbl, dist_val, 'distance')


def update_hall(hall_img_lbl, status, hall_imgs):
    hall_img = hall_imgs['0' if not status else '1']
    _update_img(hall_img_lbl, hall_img)


def update_temp(temp_img_lbl, level, temp_imgs):
    temp_img = temp_imgs[str(level)]
    _update_img(temp_img_lbl, temp_img)


def update_battery(batt_txt_lbl, batt_img_lbl, batt_val, batt_imgs):
    def map_batt_percent(percent):
        val, rem = divmod(percent, 25)
        offset = 1 if rem != 0 else 0
        return (val + offset) * 25

    # map battery percent and image
    batt_val = _map_0_to_100(batt_val)
    mapped_batt_val = map_batt_percent(batt_val)
    # update battery text label
    _update_text_label(batt_txt_lbl, batt_val, 'battery')
    # update battery image label
    batt_img = batt_imgs[str(mapped_batt_val)]
    _update_img(batt_img_lbl, batt_img)


def update_speedometer(vu_txt_lbl, vu_img_lbl, vu_val, vu_imgs):
    def map_vu_meter(speed):
        large_div, small_div = 10, 5
        val, rem = divmod(speed, large_div)
        return (val * large_div) + (rem // small_div * small_div)

    # map speedometer percent and image
    vu_val = _map_0_to_100(vu_val)
    mapped_vu_val = map_vu_meter(vu_val)
    # update battery text label
    _update_text_label(vu_txt_lbl, vu_val, 'speedometer')
    # update battery image label
    vu_img = vu_imgs[str(mapped_vu_val)]
    _update_img(vu_img_lbl, vu_img)
