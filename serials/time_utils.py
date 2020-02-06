from datetime import datetime


SEP = "\n"
DATETIME_FORMAT = "%d/%m/%Y{}%H:%M:%S".format(SEP)


def get_datetime_split(return_date=True, return_time=True):
    now = datetime.now()
    ret = ()
    if return_date:
        ret += (now.day, now.month, now.year)
    if return_time:
        ret += (now.hour, now.minute, now.second)
    return ret


def to_date_format(date_split):
    if len(date_split) == 3:
        d, m, y = date_split
    if len(date_split) == 6:
        d, m, y, _, _, _ = date_split
    return "{:02d}/{:02d}/{:04d}".format(d, m, y)


def to_time_format(time_split):
    if len(time_split) == 3:
        hr, _min, sec = time_split
    if len(time_split) == 6:
        _, _, _, hr, _min, sec = time_split
    return "{:02d}:{:02d}:{:02d}".format(hr, _min, sec)


def to_datetime_format(datetime_split, sep=SEP):
    d, m, y, hr, _min, sec = datetime_split
    return to_date_format((d, m, y)) + sep + to_time_format((hr, _min, sec))


def get_datetime(sep=SEP):
    return to_datetime_format(get_datetime_split(), sep)


def get_diff_time(s1, s2, fmt=DATETIME_FORMAT):
    return datetime.strptime(s2, fmt) - datetime.strptime(s1, fmt)


if __name__ == "__main__":
    from time import sleep

    s1 = to_datetime_format(get_datetime_split())
    print(s1)
    while True:
        sleep(1)

        s2 = to_datetime_format(get_datetime_split())
        tdelta = get_diff_time(s1, s2)
        print(s2, "->", tdelta)

