import datetime

def mask_time(target, mask="seconds"):
    ret_dt = None
    if mask == "seconds":
        ret_dt = datetime.datetime(
            year=target.year,
            month=target.month,
            day=target.day,
            hour=target.hour,
            minute=target.minute,
        )
    elif mask == "minutes":
        ret_dt = datetime.datetime(
            year=target.year,
            month=target.month,
            day=target.day,
            hour=target.hour,
        )
    elif mask == "hours":
        ret_dt = datetime.datetime(
            year=target.year,
            month=target.month,
            day=target.day,
        )
    elif mask == "days":
        ret_dt = datetime.datetime(
            year=target.year,
            month=target.month,
        )
    elif mask == "months":
        ret_dt = datetime.datetime(
            year=target.year,
        )
    else:
        raise Exception

    return ret_dt
