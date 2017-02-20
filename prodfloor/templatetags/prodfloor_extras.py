from django import template
from prodfloor.models import Stops, Times, Features
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from prodfloor.dicts import times_elem,times_m2000,times_m4000

register = template.Library()

app_list_2 = [{'app_url': '/admin/prodfloor/',
               'has_module_perms': True,
               'models':[{'perms': {'add': True, 'change': True, 'delete': True},
                          'add_url': '/admin/prodfloor/tier1/add/',
                          'admin_url': '/admin/prodfloor/tier1/',
                          'name': _('First Level Causes'),
                          'object_name': 'Tier1'},
                         {'perms': {'add': True,
                                    'change': True,
                                    'delete': True},
                          'add_url': '/admin/prodfloor/tier2/add/',
                          'admin_url': '/admin/prodfloor/tier2/',
                          'name': _('Second Level Causes'),
                          'object_name': 'Tier2'},
                         {'perms': {'add': True,
                                    'change': True,
                                    'delete': True},
                          'add_url': '/admin/prodfloor/tier3/add/',
                          'admin_url': '/admin/prodfloor/tier3/',
                          'name': _('Third Level Causes'),
                          'object_name': 'Tier3'}],
               'name':'Causes',
               'app_label': 'causes'}]
app_list_3 = []

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
        if any(obj.reason == 'Shift ended' for obj in stop):
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
def print_app(A):
    print(A)

@register.simple_tag()
def get_app(A):
    print(A)
    object_name=A[1]['models'][0]['object_name'] == 'Tier1'
    for item in A:
        if item['app_url'] == '/admin/prodfloor/':
            for item1 in item['models']:
                if item1['object_name'] == 'Tier1' or item1['object_name'] == 'Tier2' or item1['object_name'] == 'Tier3':
                    app_list_2.append(item1)
            pass
    if object_name == 'Tier1' or object_name == 'Tier2' or object_name == 'Tier3':
        app_list_2.append()
    print(A[1]['models'][0]['object_name'])

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