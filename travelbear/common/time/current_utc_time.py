from datetime import datetime
import pytz


def current_utc_time():
    return datetime.now(pytz.UTC)
