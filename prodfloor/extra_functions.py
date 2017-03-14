from django.utils import timezone
from prodfloor.models import Stops, Times, Features


def spentTime(pk,number):
    now = timezone.now()
    end = 0
    start = 0
    times = Times.objects.get(info_id=pk)
    if number == 1:
        start = times.start_time_1
        end = times.end_time_1
    elif number == 2:
        start = times.start_time_2
        end = times.end_time_2
    elif number == 3:
        start = times.start_time_3
        end = times.end_time_3
    elif number == 4:
        start = times.start_time_4
        end = times.end_time_4
    if end>start:#means that the stop_time has been set
        elapsed_time = str(end-start).split('.', 2)[0]
        return elapsed_time
    elif end == start:#means that it has not being started
        elapsed_time = '-'
        return elapsed_time
    else:#job is being worked on
        elapsed_time = str(now - start).split('.', 2)[0]
        return elapsed_time


def stopsnumber(pk):
    stops = Stops.objects.filter(info_id=pk)
    numer_of_stops = 0
    for stop in stops:
        numer_of_stops+=1
    return numer_of_stops


def timeonstop(pk):
    now = timezone.now()
    stops = Stops.objects.filter(info_id=pk)
    timeinstop = timezone.timedelta(0)
    for stop in stops:
        if stop.stop_end_time>stop.stop_start_time:
            timeinstop += stop.stop_end_time - stop.stop_start_time
        else:
            timeinstop += now - stop.stop_start_time
    return str(timeinstop).split('.', 2)[0]

def timeonstop_1(pk):
    now = timezone.now()
    stop = Stops.objects.get(pk=pk)
    timeinstop = timezone.timedelta(0)
    if stop.stop_end_time>stop.stop_start_time:
        timeinstop = stop.stop_end_time - stop.stop_start_time
    else:
        timeinstop = now - stop.stop_start_time
    return str(timeinstop).split('.', 2)[0]