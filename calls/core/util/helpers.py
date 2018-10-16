def time_between(timestamp_start, timestamp_end):
    """
    Return delta time between two timestamps as a dict with hours, minutes and seconds.
    """
    delta = timestamp_end - timestamp_start
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    hours += delta.days * 24
    return {'hours': hours, 'minutes': minutes, 'seconds': seconds}