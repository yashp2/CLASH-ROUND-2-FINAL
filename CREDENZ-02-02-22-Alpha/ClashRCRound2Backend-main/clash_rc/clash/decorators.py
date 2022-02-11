from datetime import date, timedelta, datetime
from datetime import datetime
import clash.views
from clash.models import SetTime

obj = SetTime.objects.get(pk=1)  # object containg final and intial time
a = obj.final_time.astimezone()  # to get current timezone time.
final_time = datetime(
    year=a.year, month=a.month, day=a.day, hour=a.hour, minute=a.minute, second=a.second
)  # final time
final_time_timestamp = int(final_time.timestamp())  # seconds from epoch.


def timer(view_fun):
    def time_difference(request, *args, **kwargs):
        date_now = datetime.today()
        date_now_timestamp = int(date_now.timestamp())

        # difference of seeconds
        remain_seconds = final_time_timestamp - date_now_timestamp
        a = remain_seconds
        # convert it to days and min hours
        time_delta = timedelta(seconds=remain_seconds)
        remaining_seconds = time_delta.seconds  # extract seconds

        remaining_minutes, remaining_seconds = divmod(remaining_seconds, 60)
        # print(remaining_minutes, remaining_seconds)
        remaining_hours, remaining_minutes = divmod(remaining_minutes, 60)
        print(remain_seconds)
        if a < 0:
            return clash.views.logout_view(request)
        else:
            return view_fun(request, *args, **kwargs)

    return time_difference
