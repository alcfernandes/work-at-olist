from datetime import timedelta, datetime


def time_between(timestamp_start, timestamp_end):
    """
    Return delta time between two timestamps as a dict with hours, minutes and seconds.
    """
    delta = timestamp_end - timestamp_start
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    hours += delta.days * 24
    return f'{hours}h{minutes}m{seconds}s'


def to_timedelta(date):
    """
    Convert datetime to allow subtraction operations.
    """
    time = {'hours': date.hour,
            'minutes': date.minute,
            'seconds': date.second}

    return timedelta(**time)


def current_month_year():
    """
    Returns a datetime correspond to the first day of the current month and year.
    """
    today = datetime.now()
    return datetime(today.year, today.month, 1)


def last_month_year():
    """
    Returns a datetime correspond to the first day of the last month and year.
    """
    today = datetime.now()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)

    return datetime(last_month.year, last_month.month, 1)
