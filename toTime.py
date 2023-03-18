import datetime

def conv(orig_time):
    # Convert milliseconds to seconds
    orig_time_sec = orig_time / 1000

    # Convert Unix epoch time to datetime object
    datetime_timestamp = datetime.datetime.utcfromtimestamp(orig_time_sec)

    # Subtract 7 hours to adjust for time zone difference
    datetime_adj_timestamp = datetime_timestamp - datetime.timedelta(hours = 7)

    # Convert to human-interpretable string
    # String would say: “September 01, 2022 at 12:00:00 AM”
    time_str = datetime_adj_timestamp.strftime("%B %d, %Y at %I:%M:%S %p")
    return time_str
