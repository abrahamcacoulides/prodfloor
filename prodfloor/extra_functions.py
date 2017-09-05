import pytz
from django.contrib.admin.models import LogEntry, CHANGE, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from prodfloor.models import Stops, Times, Features, Info
import datetime,copy

instance_time_zone = pytz.timezone('America/Monterrey')

def compare(text, features_to_compare, values,features_in_job):
    if None in features_to_compare:
        return True
    else:
        count = 0
        while count < len(features_to_compare):
            feature_to_compare = features_to_compare[count]
            value = values[count]
            if any(feature.features == feature_to_compare for feature in features_in_job):  # the feature to compare is IN the job features
                if value == 1:  # the feature to compare is wanted in the step and is in it
                    count += 1
                else:  # the feature to compare is NOT wanted in the step but it is there
                    # should restart the function but skipping the current step
                    return False
            else:  # the feature to compare is NOT in the job features
                if value == 0:  # the feature to compare is NOT wanted in the step and is NOT in it
                    count += 1
                else:  # the feature to compare is wanted in the step but it is NOT there
                    # should restart the function but skipping the current step
                    return False
        return True

def remaining_steps(remaining_steps,starting_index, dict, status, features_in_job):
    c=0 #number of matching steps
    index = starting_index #index provided by user in which the index in which to start is provided
    steps = dict[status] #list of steps, is determined in function of the status which is provided by the cust
    while index<len(steps):#loop to be performed if
        current = steps[index]
        features_to_compare = current[1]
        if None in features_to_compare:
            c += 1
            if index < len(steps):
                index += 1
            else:
                if c == remaining_steps:
                    return True
                else:
                    return False
        else:#this else is for the steps with features
            count = 0
            meet_the_criteria = False
            while count < len(features_to_compare):
                current = steps[index]
                features_to_compare = current[1]
                values = current[2]
                feature_to_compare = features_to_compare[count]
                value = values[count]
                if any(feature.features == feature_to_compare for feature in features_in_job):  # the feature to compare is IN the job features
                    if value == 1:  # the feature to compare is wanted in the step and is in it
                        count += 1
                        if count == len(features_to_compare):
                            meet_the_criteria = True
                    else:  # the feature to compare is NOT wanted in the step but it is there
                        # should restart the function but skipping the current step
                        break
                else:  # the feature to compare is NOT in the job features
                    if value == 0:  # the feature to compare is NOT wanted in the step and is NOT in it
                        count += 1
                        if count == len(features_to_compare):
                            meet_the_criteria = True
                    else:  # the feature to compare is wanted in the step but it is NOT there
                        # should restart the function but skipping the current step
                        break
            if meet_the_criteria:
                c += 1
            else:
                pass
            if index < len(steps):
                index += 1
            else:
                if c == remaining_steps:
                    return True
                else:
                    return False
    if c == remaining_steps:
        return True
    else:
        return False

def compare_single(text, feature_to_compare, value,features_in_job):
    if feature_to_compare == None:
        return True
    elif any(feature.features == feature_to_compare for feature in features_in_job):  # the feature to compare is IN the job features
        if value == 1:  # the feature to compare is wanted in the step and is in it
            return True
        else:  # the feature to compare is NOT wanted in the step but it is there
            # should restart the function but skipping the current step
            return False
    else:  # the feature to compare is NOT in the job features
        if value == 0:  # the feature to compare is NOT wanted in the step and is NOT in it
            return True
        else:  # the feature to compare is wanted in the step but it is NOT there
            # should restart the function but skipping the current step
            return False

def spentTime(pk,number):
    now = timezone.now()
    end = 0
    start = 0
    time_on_shift_end = timezone.timedelta(0)
    times = Times.objects.get(info_id=pk)
    job = Info.objects.get(pk=pk)
    status = job.status
    if status == 'Stoppped':
        status = job.prev_stage
    status_list = ['','Beginning','Program','Logic','Ending']
    stops_shift_end = Stops.objects.filter(info_id=pk,reason='Shift ended')
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
    else:
        pass
    for stop in stops_shift_end:
        if stop.stop_start_time > start and stop.stop_end_time<end:#el inicio del stop debe de ser mayor quue el inicio del stage y el
            if stop.stop_start_time == stop.stop_end_time: #job is in shift end stop
                time_on_shift_end += now - stop.stop_start_time
            else:
                time_on_shift_end += stop.stop_end_time - stop.stop_start_time
    if end>start:#means that the stop_time has been set
        elapsed_time = str((end-start)-time_on_shift_end).split('.', 2)[0]
        return elapsed_time
    elif end == start and status != status_list[number]:#means that it has not being started
        elapsed_time = '-'
        return elapsed_time
    else:#job is being worked on
        elapsed_time = str((now - start)-time_on_shift_end).split('.', 2)[0]
        return elapsed_time

def stopsnumber(pk):
    stops = Stops.objects.filter(info_id=pk)
    numer_of_stops = 0
    for stop in stops:
        numer_of_stops+=1
    return numer_of_stops

def timeonstop(pk):
    now = timezone.now()
    stops = Stops.objects.filter(info_id=pk).exclude(reason='Shift ended')
    timeinstop = timezone.timedelta(0)
    for stop in stops:
        if stop.stop_end_time>stop.stop_start_time:
            timeinstop += stop.stop_end_time - stop.stop_start_time
        else:
            timeinstop += now - stop.stop_start_time
    return str(timeinstop).split('.', 2)[0]

def timeonstop_1(pk):#esta en uso? no parece funcionar
    now = timezone.now()
    stop = Stops.objects.get(pk=pk)
    if stop.stop_end_time>stop.stop_start_time:
        timeinstop = stop.stop_end_time - stop.stop_start_time
    else:
        timeinstop = now - stop.stop_start_time
    return datetime.timedelta(seconds=timeinstop.total_seconds())

def timeonstop_2(pk):#esta en uso? no parece funcionar
    now = timezone.now()
    stop = Stops.objects.get(pk=pk)
    if stop.stop_end_time>stop.stop_start_time:
        timeinstop = stop.stop_end_time - stop.stop_start_time
    else:
        timeinstop = now - stop.stop_start_time
    return timeinstop.days

def totaltime(pk):
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
        number+=1
    return str(elapsed_time).split('.', 2)[0]

def effectivetime(pk):#effective time spent on job
    now = timezone.now()
    stops_end_shift = Stops.objects.filter(info_id=pk, reason='Shift ended')
    reassign_stops = Stops.objects.filter(info_id=pk, reason='Job reassignment')
    stops = Stops.objects.filter(info_id=pk).exclude(reason__in=['Shift ended', 'Job reassignment'])
    stops_1 = Stops.objects.filter(info_id=pk).exclude(reason__in=['Shift ended', ])
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
        elif end == start:  # means that it has not being started and is not in beginning stage
            elapsed_time += datetime.timedelta(0)
        else:  # job is being worked on
            elapsed_time += (now - start)
        number += 1
    for stop in stops:
        if stop.stop_end_time > stop.stop_start_time:
            timeinstop += stop.stop_end_time - stop.stop_start_time
        else:
            timeinstop += now - stop.stop_start_time
    for re_stop in reassign_stops:
        inside_another_stop = False
        if re_stop.stop_end_time > re_stop.stop_start_time:
            for stop in stops:
                if re_stop.stop_start_time >= stop.stop_start_time and re_stop.stop_end_time <= stop.stop_end_time:
                    inside_another_stop = True
        else:
            for stop in stops:
                if not (stop.stop_end_time >= stop.stop_start_time):
                    inside_another_stop = True
        if not inside_another_stop:
            if re_stop.stop_end_time > re_stop.stop_start_time:
                timeinstop += re_stop.stop_end_time - re_stop.stop_start_time
            else:
                timeinstop += now - re_stop.stop_start_time
    for es_stop in stops_end_shift:
        inside_another_stop = False
        if es_stop.stop_end_time > es_stop.stop_start_time:
            for stop in stops_1:
                if es_stop.stop_start_time > stop.stop_start_time and es_stop.stop_end_time <= stop.stop_end_time:
                    inside_another_stop = True
        else:
            for stop in stops_1:
                if not (stop.stop_end_time > stop.stop_start_time):
                    inside_another_stop = True
        if not inside_another_stop:
            if es_stop.stop_end_time > es_stop.stop_start_time:
                timeinstop += es_stop.stop_end_time - es_stop.stop_start_time
            else:
                timeinstop += now - es_stop.stop_start_time
    job = Info.objects.get(pk=pk)
    if job.status == 'Stopped':
        if any(stop.solution == 'Not available yet' for stop in reassign_stops):
            return datetime.timedelta(0)
    eff_time = elapsed_time - timeinstop
    return (eff_time)

def gettech(pk,*args, **kwargs):
    info = Info.objects.get(pk=pk)
    tech = info.Tech_name
    return tech

def categories(pk,*args, **kwargs):
    features_in_job = Features.objects.filter(info_id = pk)
    job = Info.objects.get(pk = pk)
    job_type = job.job_type
    element_dict = {
        'level_2': [],
        'level_3': [],
        'level_4': [],
        'level_5': [],
        'level_6': []}#pending
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

def multireassignfunct(request,pk,newvalues, *args, **kwargs):
    times = Times.objects.get(info__pk=pk)
    features = Features.objects.filter(info__pk=pk)
    time = timezone.now()
    job_num_info = Info.objects.get(pk = pk)
    reason = 'Job reassignment'
    po = job_num_info.po
    new_tech_obj = newvalues['new_tech']
    SU = newvalues['SU']
    new_tech = new_tech_obj.first_name + ' ' + new_tech_obj.last_name
    station = newvalues['station']
    description = 'Job # '+ job_num_info.job_num + ' reassigned to ' + new_tech + '; reason: ' + str(newvalues['reason']) + ' by: ' + SU
    if job_num_info.status != 'Stopped' and job_num_info.status != 'Reassigned':
        job_num_info.prev_stage = job_num_info.status
    else:
        pass
    if job_num_info.prev_stage == 'Beginning':
        times.end_time_1 = time
    elif job_num_info.prev_stage == 'Program':
        times.end_time_2 = time
    elif job_num_info.prev_stage == 'Logic':
        times.end_time_3 = time
    elif job_num_info.prev_stage == 'Ending':
        times.end_time_4 = time
    else:
        pass
    job_num_info.status = 'Reassigned'
    job_num_info.save()
    times.save()
    job_info_new_row = Info(job_num=job_num_info.job_num, prev_stage=job_num_info.prev_stage, Tech_name=new_tech,
                            status='Stopped', ship_date=job_num_info.ship_date,
                            current_index=job_num_info.current_index, job_type=job_num_info.job_type,
                            stage_len=job_num_info.stage_len, po=job_num_info.po, label=job_num_info.label,
                            station=station)
    job_info_new_row.save()
    ID = job_info_new_row.id
    start_time = Times(info_id=ID, start_time_1=time, end_time_1=time, start_time_2=time,
                       end_time_2=time, start_time_3=time, end_time_3=time,
                       start_time_4=time, end_time_4=time)
    start_time.save()
    job_num_stop = Stops(info_id=ID,reason=reason,extra_cause_1='N/A',extra_cause_2='N/A',solution='Not available yet',stop_start_time=time,stop_end_time= time,reason_description=description, po=po)
    job_num_stop.save()
    if any(feature == 'None' for feature in features):
        pass
    else:
        for feature in features:
            job_features_new_row = Features(info_id=ID, features=feature.features)
            job_features_new_row.save()
    ct = ContentType.objects.get_for_model(job_num_info)
    old_job_log = LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ct.pk,
        object_id=job_num_info.pk,
        object_repr=str(job_num_info.po),
        action_flag=CHANGE,
        change_message='Reassigned to ' + new_tech
    )
    old_job_log.save()
    ct = ContentType.objects.get_for_model(job_info_new_row)
    new_job_log = LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ct.pk,
        object_id=job_info_new_row.pk,
        object_repr=str(job_info_new_row.po),
        action_flag=ADDITION,
        change_message='Reassig reason: ' + description
    )
    new_job_log.save()

def gettimes(pk,B,*args, **kwargs):
    times = Times.objects.get(info_id=pk)
    if B == 'start':
        return times.start_time_1.astimezone(instance_time_zone).date()
    elif B == 'end':
        if times.start_time_1 == times.end_time_4:
            return '-'
        else:
            return times.end_time_4.astimezone(instance_time_zone).date()
    else:
        return 'N/A'