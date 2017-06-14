from django import template
from prodfloor.models import Stops, Times, Features,Info
from django.utils import timezone
from prodfloor.dicts import times_elem,times_m2000,times_m4000
import datetime,copy

register = template.Library()

@register.simple_tag()
def getpercentage(A, B, *args, **kwargs):
    return ((A+1) / B)*100

@register.simple_tag()
def getfivedigits(A, *args, **kwargs):
    return A[-5:]

@register.simple_tag()
def getcolor(A,*args, **kwargs):
    status = A.status
    ID = A.id
    po = A.po
    stop = Stops.objects.filter(info_id=ID,po=po)
    times = Times.objects.get(info_id=ID,info__po=po)
    features_objects = Features.objects.filter(info_id=ID,info__po=po)
    time_elapsed_shift_end = 0
    if any(obj.reason == 'Shift ended' for obj in stop):
        for ea in stop.filter(reason='Shift ended'):
            time_minutes = ((ea.stop_end_time - ea.stop_start_time).total_seconds() / 60)
            time_elapsed_shift_end += time_minutes
    if status == 'Complete':
        return 'progress-bar progress-bar-complete'
    elif status == 'Stopped':
        if any(obj.reason == 'Shift ended' and obj.solution=='Not available yet' for obj in stop):
            return 'progress-bar progress-bar-nassigned'
        else:
            return 'progress-bar progress-bar-stop'
    else:
        if status == 'Beginning':
            start = times.start_time_1
            TSPS = 0
            if A.job_type == '2000':
                TRS = sum(times_m2000.values())-times_m2000[status]
            elif A.job_type == '4000':
                TRS = sum(times_m4000.values())-times_m4000[status]
            elif A.job_type == 'ELEM':
                TRS = sum(times_elem.values())-times_elem[status]
        elif status == 'Program':
            start = times.start_time_2
            TSPS1 = ((times.end_time_1 - times.start_time_1).total_seconds())/60
            TSPS = TSPS1
            if A.job_type == '2000':
                TRS = sum(times_m2000.values()) - times_m2000[status]
            elif A.job_type == '4000':
                TRS = sum(times_m4000.values()) - times_m4000[status]
            elif A.job_type == 'ELEM':
                TRS = sum(times_elem.values()) - times_elem[status]
        elif status == 'Logic':
            start = times.start_time_3
            TSPS1 = ((times.end_time_1 - times.start_time_1).total_seconds()) / 60
            TSPS2 = ((times.end_time_2 - times.start_time_2).total_seconds()) / 60
            TSPS = TSPS1 + TSPS2
            if A.job_type == '2000':
                TRS = sum(times_m2000.values()) - times_m2000[status]
            elif A.job_type == '4000':
                TRS = sum(times_m4000.values()) - times_m4000[status]
            elif A.job_type == 'ELEM':
                TRS = sum(times_elem.values()) - times_elem[status]
        elif status == 'Ending':
            start = times.start_time_4
            TSPS1 = ((times.end_time_1 - times.start_time_1).total_seconds()) / 60
            TSPS2 = ((times.end_time_2 - times.start_time_2).total_seconds()) / 60
            TSPS3 = ((times.end_time_3 - times.start_time_3).total_seconds()) / 60
            TSPS = TSPS1 + TSPS2 + TSPS3
            if A.job_type == '2000':
                TRS = sum(times_m2000.values()) - times_m2000[status]
            elif A.job_type == '4000':
                TRS = sum(times_m4000.values()) - times_m4000[status]
            elif A.job_type == 'ELEM':
                TRS = sum(times_elem.values()) - times_elem[status]
        else:
            pass
        if A.job_type == '2000':
            ETC = sum(times_m2000.values())
            if any(feature.features == 'COP' for feature in features_objects):
                pass
            else:
                ETC -= 25
            if any(feature.features == 'SHC' for feature in features_objects):
                pass
            else:
                ETC -= 10
        elif A.job_type == '4000':
            ETC = sum(times_m4000.values())
            if any(feature.features == 'COP' for feature in features_objects):
                pass
            else:
                ETC = ETC - 10
            if any(feature.features == 'SHC' for feature in features_objects):
                pass
            else:
                ETC = ETC - 20
        elif A.job_type == 'ELEM':
            ETC = sum(times_elem.values())
            if any(feature.features == 'HAPS' for feature in features_objects):
                pass
            else:
                ETC = ETC - 15

        now = timezone.now()
        elapsed_time = now - start
        elapsed_time_minutes = (elapsed_time.total_seconds()/60)
        PTC = TSPS + elapsed_time_minutes + TRS - time_elapsed_shift_end
        if PTC < ETC:
            return 'progress-bar progress-bar-working'
        elif PTC < (ETC*1.25):
            return 'progress-bar progress-bar-delayed'
        else:
            return 'progress-bar progress-bar-vdelayed'

@register.simple_tag()
def getstation(A,*args, **kwargs):
    stations = {'1': 'S1',
                '2': 'S2',
                '3': 'S3',
                '4': 'S4',
                '5': 'S5',
                '6': 'S6',
                '7': 'S7',
                '8': 'S8',
                '9': 'S9',
                '10': 'S10',
                '11': 'S11',
                '12': 'S12',
                '13': 'ELEM1',
                '14': 'ELEM2'}
    return stations[A]

@register.simple_tag()
def resultingtime(pk,number, *args, **kwargs):
    now = timezone.now()
    end = 0
    start = 0
    times = Times.objects.get(info_id=pk)
    stops = Stops.objects.filter(info_id=pk,reason='Shift ended')
    minutes_on_shift_end = datetime.timedelta(0)
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
    for stop in stops:
        if stop.stop_start_time > start and stop.stop_end_time < end:
            if stop.stop_start_time == stop.stop_end_time: #job is in shift end stop
                if stop.stop_start_time > start:
                    minutes_on_shift_end += now - stop.stop_start_time
            else:
                if stop.stop_start_time > start and stop.stop_end_time < end:
                    minutes_on_shift_end += stop.stop_end_time - stop.stop_start_time
    if end>start:#means that the stop_time has been set
        elapsed_time = str((end-start)-minutes_on_shift_end).split('.', 2)[0]
        return elapsed_time
    elif end == start:#means that it has not being started
        elapsed_time = '-'
        return elapsed_time
    else:#job is being worked on
        elapsed_time = str((now - start)-minutes_on_shift_end).split('.', 2)[0]
        return elapsed_time

@register.simple_tag()
def totaltime(pk, *args, **kwargs):
    now = timezone.now()
    end = 0
    start = 0
    times = Times.objects.get(info_id=pk)
    elapsed_time = datetime.timedelta(0)
    number = 1
    while number < 5:
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
        if end > start:  # means that the stop_time has been set
            elapsed_time += (end - start)
        elif end == start and number != 1:  # means that it has not being started and is not in beginning stage
            elapsed_time += datetime.timedelta(0)
        else:  # job is being worked on
            elapsed_time += (now - start)
        number += 1
    return str(elapsed_time).split('.', 2)[0]

@register.simple_tag()
def stopsnumber(pk,*args, **kwargs):
    stops = Stops.objects.filter(info_id=pk)
    numer_of_stops = 0
    for stop in stops:
        numer_of_stops+=1
    return numer_of_stops

@register.simple_tag()
def timeonstop(pk,*args, **kwargs):
    now = timezone.now()
    stops = Stops.objects.filter(info_id=pk)
    timeinstop = timezone.timedelta(0)
    for stop in stops:
        if stop.stop_end_time>stop.stop_start_time:
            timeinstop += stop.stop_end_time - stop.stop_start_time
        else:
            timeinstop += now - stop.stop_start_time
    return str(timeinstop).split('.', 2)[0]

@register.simple_tag()
def getinfo(pk,info,*args, **kwargs):
    stations = {'1': 'S1',
                '2': 'S2',
                '3': 'S3',
                '4': 'S4',
                '5': 'S5',
                '6': 'S6',
                '7': 'S7',
                '8': 'S8',
                '9': 'S9',
                '10': 'S10',
                '11': 'S11',
                '12': 'S12',
                '13': 'ELEM1',
                '14': 'ELEM2'}
    job = Info.objects.get(pk=pk)
    dict = {'job_num':job.job_num,
            'job_type':job.job_type,
            'station':stations[job.station]}
    return dict[info]

@register.simple_tag()
def timeonstop_1(pk,*args, **kwargs):
    now = timezone.now()
    stop = Stops.objects.get(pk=pk)
    timeinstop = timezone.timedelta(0)
    if stop.stop_end_time>stop.stop_start_time:
        timeinstop = stop.stop_end_time - stop.stop_start_time
    else:
        timeinstop = now - stop.stop_start_time
    return str(timeinstop).split('.', 2)[0]

@register.simple_tag()
def effectivetime(pk,*args, **kwargs):
    now = timezone.now()
    stops = Stops.objects.filter(info_id=pk)
    timeinstop = timezone.timedelta(0)
    end = 0
    start = 0
    times = Times.objects.get(info_id=pk)
    elapsed_time = datetime.timedelta(0)
    number = 1
    while number < 5:
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
        if end > start:  # means that the stop_time has been set
            elapsed_time += (end - start)
        elif end == start and number != 1:  # means that it has not being started and is not in beginning stage
            elapsed_time += datetime.timedelta(0)
        else:  # job is being worked on
            elapsed_time += (now - start)
        number += 1
    for stop in stops:
        if stop.stop_start_time > start and stop.stop_end_time < end:
            if stop.stop_end_time > stop.stop_start_time:
                timeinstop += stop.stop_end_time - stop.stop_start_time
            else:
                timeinstop += now - stop.stop_start_time
    eff_time = str(elapsed_time - timeinstop).split('.', 2)[0]
    return (eff_time)

@register.simple_tag()
def gettech(pk,*args, **kwargs):
    info = Info.objects.get(pk=pk)
    tech = info.Tech_name
    return tech

@register.simple_tag()
def categories(pk,*args, **kwargs):
    features_in_job = Features.objects.filter(info_id = pk)
    job = Info.objects.get(pk = pk)
    job_type = job.job_type
    element_dict = {
        'level_2': [],
        'level_3': [],
        'level_4': [],
        'level_5': [],
        'level_6': []}
    m2000_dict = {
        'level_2': ['REAR', 'DUP', 'MOD', '2STARTERS', 'SHC', 'EMCO', 'R6'],
        'level_3': ['mView', 'iMon', 'LOC'],
        'level_4': ['MANUAL', 'OVL'],
        'level_5': ['CUST', 'MRL'],
        'level_6': ['TSSA']}
    m4000_dict = {
        'level_2': ['REAR', 'DUP', 'MOD', '2STARTERS'],
        'level_3': ['mView', 'iMon', 'LOC', 'SHORTF'],
        'level_4': ['MANUAL', 'OVL'],
        'level_5': ['CUST'],
        'level_6': ['TSSA']}
    if job_type == '2000':
        dict = copy.deepcopy(m2000_dict)
    elif job_type == '4000':
        dict = copy.deepcopy(m4000_dict)
    else:
        dict = copy.deepcopy(element_dict)
    if any(feature.features in dict['level_6'] for feature in features_in_job):
        category = 6
    elif any(feature.features in dict['level_5'] for feature in features_in_job):
        category = 5
    elif any(feature.features in dict['level_4'] for feature in features_in_job):
        category = 4
    elif any(feature.features in dict['level_3'] for feature in features_in_job):
        category = 3
    elif any(feature.features in dict['level_2'] for feature in features_in_job):
        category = 2
    else:
        category = 1
    return category

@register.simple_tag()
def ETF(pk,*args, **kwargs):#function to return the expected time remaining
    return '0'