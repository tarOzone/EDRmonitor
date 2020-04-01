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


def to_date_format(date_split, date_sep="/"):
    if len(date_split) == 3:
        d, m, y = date_split
    if len(date_split) == 6:
        d, m, y, _, _, _ = date_split
    return f"{d:02d}{date_sep}{m:02d}{date_sep}{y:04d}"


def to_time_format(time_split, time_sep=":"):
    if len(time_split) == 3:
        hr, _min, sec = time_split
    if len(time_split) == 6:
        _, _, _, hr, _min, sec = time_split
    return f"{hr:02d}{time_sep}{_min:02d}{time_sep}{sec:02d}"


def to_datetime_format(datetime_split, sep=SEP, date_sep="/", time_sep=":"):
    d, m, y, hr, _min, sec = datetime_split
    return to_date_format((d, m, y), date_sep) + sep + to_time_format((hr, _min, sec), time_sep)


def get_datetime(datetime_sep=SEP, date_sep="/", time_sep=":"):
    return to_datetime_format(get_datetime_split(), datetime_sep, date_sep, time_sep)


def get_diff_time(s1, s2, fmt=DATETIME_FORMAT):
    return datetime.strptime(s2, fmt) - datetime.strptime(s1, fmt)

