from django.utils import timezone
import datetime

now = datetime.datetime.now()
date = datetime.datetime(2017, 1, 26, 12, 8, 59, 0)
elapsed = now - date
minutes = 5

if (elapsed.total_seconds()/60) < minutes:
    print('Yes')
else:
    print('No')


#************************** working funtion for colors
'''
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
        now = timezone.now()
        elapsed_time = now - start
        if A.job_type == '2000':
            if (elapsed_time.total_seconds()/60) < times_m2000[A.status]:
                return 'progress-bar progress-bar-working'
            elif (elapsed_time.total_seconds()/60) < (times_m2000[A.status]+60):
                return 'progress-bar progress-bar-delayed'
            else:
                return 'progress-bar progress-bar-vdelayed'
        elif A.job_type == '4000':
            if (elapsed_time.total_seconds()/60) < times_m4000[A.status]:
                return 'progress-bar progress-bar-working'
            elif (elapsed_time.total_seconds()/60) < (times_m4000[A.status]+60):
                return 'progress-bar progress-bar-delayed'
            else:
                return 'progress-bar progress-bar-vdelayed'
        elif A.job_type == 'ELEM':
            if (elapsed_time.total_seconds()/60) < times_elem[A.status]:
                return 'progress-bar progress-bar-working'
            elif (elapsed_time.total_seconds()/60) < (times_elem[A.status]+60):
                return 'progress-bar progress-bar-delayed'
            else:
                return 'progress-bar progress-bar-vdelayed'
        else:
            pass
    elif status == 'Program':
        start = times.start_time_2
        now = timezone.now()
        elapsed_time = now - start
        if A.job_type == '2000':
            if (elapsed_time.total_seconds()/60) < times_m2000[A.status]:
                return 'progress-bar progress-bar-working'
            elif (elapsed_time.total_seconds()/60) < (times_m2000[A.status]+60):
                return 'progress-bar progress-bar-delayed'
            else:
                return 'progress-bar progress-bar-vdelayed'
        elif A.job_type == '4000':
            if (elapsed_time.total_seconds()/60) < times_m4000[A.status]:
                return 'progress-bar progress-bar-working'
            elif (elapsed_time.total_seconds()/60) < (times_m4000[A.status]+60):
                return 'progress-bar progress-bar-delayed'
            else:
                return 'progress-bar progress-bar-vdelayed'
        elif A.job_type == 'ELEM':
            if (elapsed_time.total_seconds()/60) < times_elem[A.status]:
                return 'progress-bar progress-bar-working'
            elif (elapsed_time.total_seconds()/60) < (times_elem[A.status]+60):
                return 'progress-bar progress-bar-delayed'
            else:
                return 'progress-bar progress-bar-vdelayed'
        else:
            pass
    elif status == 'Logic':
        start = times.start_time_3
        now = timezone.now()
        elapsed_time = now - start
        if A.job_type == '2000':
            if (elapsed_time.total_seconds()/60) < times_m2000[A.status]:
                return 'progress-bar progress-bar-working'
            elif (elapsed_time.total_seconds()/60) < (times_m2000[A.status]+60):
                return 'progress-bar progress-bar-delayed'
            else:
                return 'progress-bar progress-bar-vdelayed'
        elif A.job_type == '4000':
            if (elapsed_time.total_seconds()/60) < times_m4000[A.status]:
                return 'progress-bar progress-bar-working'
            elif (elapsed_time.total_seconds()/60) < (times_m4000[A.status]+60):
                return 'progress-bar progress-bar-delayed'
            else:
                return 'progress-bar progress-bar-vdelayed'
        else:
            pass
    elif status == 'Ending':
        start = times.start_time_4
        now = timezone.now()
        elapsed_time = now - start
        if A.job_type == '2000':
            if (elapsed_time.total_seconds()/60) < times_m2000[A.status]:
                return 'progress-bar progress-bar-working'
            elif (elapsed_time.total_seconds()/60) < (times_m2000[A.status]+60):
                return 'progress-bar progress-bar-delayed'
            else:
                return 'progress-bar progress-bar-vdelayed'
        elif A.job_type == '4000':
            if (elapsed_time.total_seconds()/60) < times_m4000[A.status]:
                return 'progress-bar progress-bar-working'
            elif (elapsed_time.total_seconds()/60) < (times_m4000[A.status]+60):
                return 'progress-bar progress-bar-delayed'
            else:
                return 'progress-bar progress-bar-vdelayed'
        elif A.job_type == 'ELEM':
            if (elapsed_time.total_seconds()/60) < times_elem[A.status]:
                return 'progress-bar progress-bar-working'
            elif (elapsed_time.total_seconds()/60) < (times_elem[A.status]+60):
                return 'progress-bar progress-bar-delayed'
            else:
                return 'progress-bar progress-bar-vdelayed'
        else:
            pass
    pass'''