from django.contrib.auth.models import User
from django.forms import formset_factory
from django.http import Http404, HttpResponseRedirect,HttpResponse
from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from prodfloor.forms import Maininfo, FeaturesSelection, StopReason, ResumeSolution, ReassignJob, Records, StopRecord, SUStop, MultipleReassign
from django.contrib.auth import logout
from stopscauses.models import Tier3,Tier2,Tier1
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from prodfloor.dicts import stations_by_type,headers,stops_headers,dict_m2000_new,dict_elem_new,dict_m4000_new,mureassign_headers
import json,io
from .extra_functions import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext_lazy as _
from xlsxwriter.workbook import Workbook

def prodfloor_view(request):
    job_list = Info.objects.exclude(status="Complete").order_by('job_num')
    context = {'job_list': job_list}
    return render(request, 'prodfloor/prodfloor.html', context)

def M2000View(request):
    job_list = Info.objects.filter(job_type='2000').exclude(status='Complete').order_by('ship_date')
    context = {'job_list': job_list}
    return render(request, 'prodfloor/prodfloor.html', context)

def M4000View(request):
    job_list = Info.objects.filter(job_type='4000').exclude(status='Complete').order_by('ship_date')
    context = {'job_list': job_list}
    return render(request, 'prodfloor/prodfloor.html', context)

def ELEMView(request):
    job_list = Info.objects.filter(job_type='ELEM').exclude(status='Complete').order_by('ship_date')
    context = {'job_list': job_list}
    return render(request, 'prodfloor/prodfloor.html', context)

@login_required()
def detail(request):#reports view
    job = Info.objects.all()
    if request.method == 'POST':#this if is for the filtering, the arguments to filter are received through it
        form = Records(request.POST)
        if form.is_valid():
            job_num = form.cleaned_data['job_num']
            po = form.cleaned_data['po']
            status = form.cleaned_data['status']
            job_type = form.cleaned_data['job_type']
            station = form.cleaned_data['station']
            before = form.cleaned_data['before']
            after = form.cleaned_data['after']
            tech = form.cleaned_data['tech']
            if job_num != '':
                job = job.filter(job_num__contains=job_num)
            if tech != None:
                tech_obj = User.objects.get(username=tech)
                job = job.filter(Tech_name=tech_obj.get_full_name())
            if po != '':
                job = job.filter(po__contains=po)
            if status:
                job = job.filter(status__in=status)
            if job_type:
                job = job.filter(job_type__in=job_type)
            if station:
                job = job.filter(station__in=station)
            if after:
                if before:
                    times = Times.objects.filter(start_time_1__gte=after,start_time_1__lte=before)
                    times_pks=[]
                    for i in times:
                        times_pks.append(i.info.pk)
                    job = job.filter(pk__in=times_pks)
                else:
                    times = Times.objects.filter(start_time_1__gte=after)
                    times_pks = []
                    for i in times:
                        times_pks.append(i.info.pk)
                    job = job.filter(pk__in=times_pks)
            else:
                if before:
                    times = Times.objects.filter(start_time_1__lte=before)
                    times_pks = []
                    for i in times:
                        times_pks.append(i.info.pk)
                    job = job.filter(pk__in=times_pks)
            request.session['report_objects'] = []
            for item in job:
                request.session['report_objects'].append(item.pk)
            paginator = Paginator(job, 25)
            jobs = paginator.page(1)
            return render(request, 'prodfloor/detail.html', {'result_headers': headers,'jobs':jobs,'form':form,'job':job})
        else:
            request.session['report_objects'] = []
            for item in job:
                request.session['report_objects'].append(item.pk)
            return render(request, 'prodfloor/detail.html', {'result_headers': headers,'jobs':job,'form':form,'job':job})
    else:#this else refers to when the page is been requested, usually on the first access and when pagination is clicked ('next' or 'previous')
        page = request.GET.get('page')
        try:
            try:
                if request.session['report_objects']:
                    job = []
                    pks = request.session['report_objects']
                    for pk in pks:
                        job.append(Info.objects.get(pk=pk))
            except KeyError:
                pass
            form = Records
            paginator = Paginator(job, 25)
            request.session['report_objects'] = []
            for item in job:
                request.session['report_objects'].append(item.pk)
            jobs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            form = Records
            paginator = Paginator(job, 25)
            request.session['report_objects'] = []
            for item in job:
                request.session['report_objects'].append(item.pk)
            jobs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            form = Records
            paginator = Paginator(job, 5)
            jobs = paginator.page(paginator.num_pages)
        return render(request, 'prodfloor/detail.html', {'result_headers': headers, 'jobs': jobs,'form':form,'job':job})

@login_required()
def stops_reports(request):#reports for the stops view
    job = Info.objects.all()
    stops = Stops.objects.all()
    if request.method == 'POST':#this if is for the filtering, the arguments to filter are received through it
        form = StopRecord(request.POST)
        if form.is_valid():
            job_num = form.cleaned_data['job_num']
            po = form.cleaned_data['po']
            reason = form.cleaned_data['reason'].values_list('tier_one_cause',flat=True)
            job_type = form.cleaned_data['job_type']
            station = form.cleaned_data['station']
            before = form.cleaned_data['before']
            after = form.cleaned_data['after']
            completed_after = form.cleaned_data['completed_after']
            completed_before = form.cleaned_data['completed_before']
            if job_num != '':
                job=job.filter(job_num__contains=job_num)
                jobs_lst = []
                for j in job:
                    jobs_lst.append(j.pk)
                stops = stops.filter(info_id__in=jobs_lst)
            if po != '':
                stops = stops.filter(po__contains=po)
            if reason:
                stops = stops.filter(reason__in=reason)
            if job_type:
                job = job.filter(job_type__in=job_type)
                jobs_lst = []
                for j in job:
                    jobs_lst.append(j.pk)
                stops = stops.filter(info_id__in=jobs_lst)
            if station:
                job = job.filter(station__in=station)
                jobs_lst = []
                for j in job:
                    jobs_lst.append(j.pk)
                stops = stops.filter(info_id__in=jobs_lst)
            if after:
                if before:
                    stops = stops.filter(stop_start_time__gte=after,stop_start_time__lte=before)
                else:
                    stops = stops.filter(stop_start_time__gte=after)
            else:
                if before:
                    stops = stops.filter(stop_start_time__lte=before)
            if completed_after:
                if completed_before:
                    stops = stops.filter(stop_end_time__gte=completed_after,stop_end_time__lte=completed_before)
                else:
                    stops = stops.filter(stop_end_time__gte=completed_after)
            else:
                if completed_before:
                    stops = stops.filter(stop_end_time__lte=completed_before)
            request.session['stops_objects'] = []
            for item in stops:
                request.session['stops_objects'].append(item.pk)
            paginator = Paginator(stops, 25)
            stop = paginator.page(1)
            return render(request, 'prodfloor/stops_record.html', {'result_headers': stops_headers,'jobs':stop,'form':form,'job':stops})
        else:
            request.session['stops_objects'] = []
            paginator = Paginator(stops, 25)
            stop = paginator.page(1)
            for item in stops:
                request.session['stops_objects'].append(item.pk)
            return render(request, 'prodfloor/stops_record.html', {'result_headers': stops_headers,'jobs':stop,'form':form,'job':stops})
    else:#this else refers to when the page is been requested, usually on the first access and when pagination is clicked ('next' or 'previous')
        try:
            if request.session['stops_objects']:
                stops = []
                pks = request.session['stops_objects']
                for pk in pks:
                    stops.append(Stops.objects.get(pk=pk))
        except KeyError:
            pass
        form = StopRecord
        paginator = Paginator(stops, 25)
        request.session['stops_objects'] = []
        for item in stops:
            request.session['stops_objects'].append(item.pk)
        page = request.GET.get('page')
        try:
            stop = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            stop = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            stop = paginator.page(paginator.num_pages)
        return render(request, 'prodfloor/stops_record.html', {'result_headers': stops_headers, 'jobs': stop,'form':form,'job':stops})

def generatexml(request):
    stations_dict = {'0':'-----',
                   '1':'S1',
            '2':'S2',
            '3':'S3',
            '4':'S4',
            '5':'S5',
            '6':'S6',
            '7':'S7',
            '8':'S8',
            '9':'S9',
            '10':'S10',
            '11':'S11',
            '12':'S12',
            '13':'ELEM1',
            '14':'ELEM2'}
    job_type_dict = {'2000':'M2000',
            '4000':'M4000',
            'ELEM':'Element'}
    jobs= request.session['report_objects']
    output = io.BytesIO()
    book = Workbook(output)
    title_format = book.add_format({'bold':True,'border':True,'bg_color':'#d8d8d8','align':'center'})
    other_format = book.add_format({'border':True})
    sheet = book.add_worksheet('Report')
    i = 0
    for header in headers:
        sheet.write(0, i, header, title_format)
        i+=1
    c=1
    while c < len(jobs)+1:
        for pk in jobs:
            job = Info.objects.get(pk=pk)
            beginning_time = spentTime(pk,1)
            program_time = spentTime(pk, 2)
            logic_time = spentTime(pk, 3)
            ending_time = spentTime(pk, 4)
            number_of_stops = stopsnumber(pk)
            time_on_stop = timeonstop(pk)
            elapsed_time = totaltime(pk)
            eff_time = effectivetime(pk)
            tech = gettech(pk)
            category = categories(pk)
            sheet.write(c, 0, job.job_num,other_format)
            sheet.write(c, 1, job.po,other_format)
            sheet.write(c, 2, job_type_dict[job.job_type],other_format)
            sheet.write(c, 3, job.status,other_format)
            sheet.write(c, 4, stations_dict[job.station],other_format)
            sheet.write(c, 5, str(job.ship_date).split('.', 2)[0], other_format)
            sheet.write(c, 6, beginning_time, other_format)
            sheet.write(c, 7, program_time, other_format)
            sheet.write(c, 8, logic_time, other_format)
            sheet.write(c, 9, ending_time, other_format)
            sheet.write(c, 10, elapsed_time, other_format)
            sheet.write(c, 11, number_of_stops, other_format)
            sheet.write(c, 12, time_on_stop, other_format)
            sheet.write(c, 13, eff_time, other_format)
            sheet.write(c, 14, category, other_format)
            sheet.write(c, 15, tech, other_format)
            c+=1
    sheet.set_column(0,0,10.29)
    sheet.set_column(3,3,13.14)
    sheet.autofilter('A1:O1')
    book.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=Report%s.xlsx"%str(timezone.now())

    return response

def generatestopsxml(request):
    stations_dict = {'0':'-----',
                   '1':'S1',
            '2':'S2',
            '3':'S3',
            '4':'S4',
            '5':'S5',
            '6':'S6',
            '7':'S7',
            '8':'S8',
            '9':'S9',
            '10':'S10',
            '11':'S11',
            '12':'S12',
            '13':'ELEM1',
            '14':'ELEM2'}
    job_type_dict = {'2000':'M2000',
            '4000':'M4000',
            'ELEM':'Element'}
    stops= request.session['stops_objects']
    output = io.BytesIO()
    book = Workbook(output)
    title_format = book.add_format({'bold':True,'border':True,'bg_color':'#d8d8d8','align':'center'})
    other_format = book.add_format({'border':True})
    sheet = book.add_worksheet('Report')
    i = 0
    for header in stops_headers:
        sheet.write(0, i, header, title_format)
        i+=1
    c=1
    while c < len(stops)+1:
        for pk in stops:
            stop = Stops.objects.get(pk=pk)
            job = Info.objects.get(pk=stop.info_id)
            time_on_stop = timeonstop_1(pk)
            sheet.write(c, 0, job.job_num,other_format)
            sheet.write(c, 1, stop.po,other_format)
            sheet.write(c, 2, job_type_dict[job.job_type],other_format)
            sheet.write(c, 3, stop.reason,other_format)
            sheet.write(c, 4, stop.extra_cause_1, other_format)
            sheet.write(c, 5, stop.extra_cause_2, other_format)
            sheet.write(c, 6, stop.reason_description, other_format)
            sheet.write(c, 7, stop.solution, other_format)
            sheet.write(c, 8, stations_dict[job.station],other_format)
            sheet.write(c, 9, time_on_stop, other_format)
            sheet.write(c, 10, gettech(pk), other_format)
            c+=1
    sheet.set_column(0,0,10.29)
    sheet.set_column(3,3,13.14)
    sheet.autofilter('A1:J1')
    book.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=Stops_Report%s.xlsx"%str(timezone.now())

    return response

@login_required()
def Start(request):
    if 'pp_jobinfo' in request.session:
        dict_of_steps = {}
        job_num = request.session['temp_job_num']
        po = request.session['temp_po']
        pk = request.session['temp_pk']
        job = Info.objects.get(pk = pk)
        features_objects = Features.objects.filter(info__pk=pk)
        if job.job_type == '2000':
            dict_of_steps = dict_m2000_new
        elif job.job_type == '4000':
            dict_of_steps = dict_m4000_new
        elif job.job_type == 'ELEM':
            dict_of_steps = dict_elem_new
        status = job.status
        list_of_steps = dict_of_steps[status]
        job.stage_len = len(list_of_steps)
        steps_length = job.stage_len
        request.session['already_here'] = True
        job.current_index = 0
        while True:
            current_data = list_of_steps[job.current_index]
            if compare(current_data[0], current_data[1], current_data[2], features_objects):
                text = current_data[0]
                break
            else:
                job.current_index += 1
                job.save()
        current_step = job.current_index + 1
        job.save()
        del request.session['pp_jobinfo']
        return render(request, 'prodfloor/newjob.html', {'job_num': job_num, 'job': job, 'steps': steps_length,
                                                         'current_step_text': text,
                                                         'current_step': current_step})
    else:
        raise Http404("This is not the droid you're looking for")

@login_required()
def Continue(request,pk,po):
    if request.user.is_authenticated() and request.user.is_active:
        job = Info.objects.get(pk=pk)
        request.session['temp_pk'] = job.pk
        request.session['temp_job_num'] = job.job_num
        request.session['temp_po'] = po
        job_num = job.job_num
        dict_of_steps = {}
        features_objects = Features.objects.filter(info_id=job.id)
        if job.job_type == '2000':
            dict_of_steps = copy.deepcopy(dict_m2000_new)
        elif job.job_type == '4000':
            dict_of_steps = copy.deepcopy(dict_m4000_new)
        elif job.job_type == 'ELEM':
            dict_of_steps = copy.deepcopy(dict_elem_new)
        status = job.status
        list_of_steps = dict_of_steps[status]
        while True:
            if status == 'Stopped':
                current_data = list_of_steps[0]
                text = current_data[0]
                break
            else:
                current_data = list_of_steps[job.current_index]
                if compare(current_data[0],current_data[1],current_data[2],features_objects):
                    text = current_data[0]
                    break
                else:
                    job.current_index +=1
                    job.save()
        steps_length = len(list_of_steps)
        job.stage_len = steps_length
        job.save()
        current_step = job.current_index + 1
        if  job.Tech_name == request.user.first_name + ' ' + request.user.last_name:
            if job.status == 'Stopped':
                active_jobs = Info.objects.filter(Tech_name=request.user.first_name + ' ' + request.user.last_name).exclude(status='Complete').exclude(status='Stopped')
                c = 0
                for object in active_jobs:
                    c += 1
                if c > 0:
                    messages.warning(request,
                                     'You already have one active Job. In order to continue with this one stop or finish the active one.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    stop = Stops.objects.filter(info_id=job.id, solution='Not available yet')
                    if any(object.reason == 'Job reassignment' for object in stop):
                        stop_reass = Stops.objects.get(info_id=job.id, solution='Not available yet',reason='Job reassignment')
                        stop_reass.stop_end_time = timezone.now()
                        stop_reass.solution = 'Job resumed.'
                        stop_reass.save()
                        if any(object.reason != 'Job reassignment' for object in stop):
                            if any(object.reason == 'Shift ended' for object in stop):
                                solution = "Shift restart/Reassigned"
                                ID = job.id
                                stop_shiftend = Stops.objects.get(info_id=ID, solution='Not available yet', reason='Shift ended')
                                stop_shiftend.solution = solution
                                stop_shiftend.stop_end_time = timezone.now()
                                stop_shiftend.save()
                                stop_1 = Stops.objects.filter(info_id=job.id, solution='Not available yet').exclude(reason='Job reassignment')
                                if any(object.reason != 'Shift ended' for object in stop_1):
                                    index_num = 0
                                    current_step = index_num+1
                                    status = 'Stopped'
                                    list_of_steps = dict_of_steps[status]
                                    steps_length = len(list_of_steps)
                                    return render(request, 'prodfloor/newjob.html',
                                                  {'job_num': job_num, 'job': job, 'steps': steps_length,
                                                   'current_step_text': list_of_steps[index_num],
                                                   'current_step': current_step})
                                else:
                                    job.status = job.prev_stage
                                    job.prev_stage = 'Stopped'
                                    list_of_steps = dict_of_steps[job.status]
                                    job.stage_len = len(list_of_steps)
                                    job.save()
                                    steps_length = job.stage_len
                                    while True:
                                       current_data = list_of_steps[job.current_index]
                                       if compare(current_data[0],current_data[1],current_data[2],features_objects):
                                           text = current_data[0]
                                           break
                                       else:
                                           job.current_index +=1
                                           job.save()
                                    current_step = job.current_index + 1
                                    return render(request, 'prodfloor/newjob.html',{'job_num': job_num, 'job': job, 'steps': steps_length,'current_step_text': text, 'current_step': current_step})
                            else:
                                index_num = 0
                                current_step = index_num+1
                                status = 'Stopped'
                                list_of_steps = dict_of_steps[status]
                                steps_length = len(list_of_steps)
                                return render(request, 'prodfloor/newjob.html',
                                              {'job_num': job_num, 'job': job, 'steps': steps_length,
                                               'current_step_text': list_of_steps[index_num],
                                               'current_step': current_step})
                        else:
                            job.status = job.prev_stage
                            job.prev_stage = 'Stopped'
                            list_of_steps = dict_of_steps[job.status]
                            job.stage_len = len(list_of_steps)
                            job.save()
                            steps_length = job.stage_len
                            while True:
                                current_data = list_of_steps[job.current_index]
                                if compare(current_data[0], current_data[1], current_data[2], features_objects):
                                    text = current_data[0]
                                    break
                                else:
                                    job.current_index += 1
                                    job.save()
                            current_step = job.current_index+1
                            return render(request, 'prodfloor/newjob.html',{'job_num': job_num, 'job': job, 'steps': steps_length,
                                           'current_step_text': text, 'current_step': current_step})
                    elif any(object.reason == 'Shift ended' for object in stop):
                        stop_shiftend = Stops.objects.get(info_id=job.id, solution='Not available yet',reason='Shift ended')
                        stop_shiftend.solution = 'Shift restart/Reassigned.'
                        stop_shiftend.stop_end_time = timezone.now()
                        stop_shiftend.save()
                        stop_2 = Stops.objects.filter(info_id=job.id, solution='Not available yet').exclude(reason='Job reassignment').exclude(reason='Shift ended')
                        if any(object.reason != 'Shift ended' for object in stop_2):
                            index_num = 0
                            current_step = index_num + 1
                            status= 'Stopped'
                            list_of_steps = dict_of_steps[status]
                            steps_length = len(list_of_steps)
                            return render(request, 'prodfloor/newjob.html',
                                          {'job_num': job_num, 'job': job, 'steps': steps_length,
                                           'current_step_text': list_of_steps[index_num],
                                           'current_step': current_step})
                        else:
                            job.status = job.prev_stage
                            job.prev_stage = 'Stopped'
                            list_of_steps = dict_of_steps[job.status]
                            job.stage_len = len(list_of_steps)
                            job.save()
                            steps_length = job.stage_len
                            while True:
                                current_data = list_of_steps[job.current_index]
                                if compare(current_data[0], current_data[1], current_data[2], features_objects):
                                    text = current_data[0]
                                    break
                                else:
                                    job.current_index += 1
                                    job.save()
                            current_step = job.current_index+1
                            return render(request, 'prodfloor/newjob.html',{'job_num': job_num, 'job': job, 'steps': steps_length,'current_step_text': text,'current_step': current_step})
                    else:
                        index_num = 0
                        current_step = index_num + 1
                        status = 'Stopped'
                        list_of_steps = dict_of_steps[status]
                        steps_length = len(list_of_steps)
                        return render(request, 'prodfloor/newjob.html',
                                      {'job_num': job_num, 'job': job, 'steps': steps_length,
                                       'current_step_text': list_of_steps[index_num],
                                       'current_step': current_step})
            else:
                return render(request, 'prodfloor/newjob.html', {'job_num': job_num, 'job': job, 'steps': steps_length,
                                                         'current_step_text': text,
                                                         'current_step': current_step})
        else:
            messages.warning(request, 'The Job you tried to reach is assigned to someone else.')
            return HttpResponseRedirect('/admin/')
    else:
        raise Http404("How you got here?")

@login_required()
def EndShift(request):
    tech_name = request.user.first_name + ' ' + request.user.last_name
    jobs = Info.objects.filter(Tech_name= tech_name).exclude(status='Complete').exclude(status='Stopped')
    for obj in jobs:
        if obj.status != 'Stopped':
            obj.prev_stage = obj.status
        obj.status = 'Stopped'
        ID = obj.id
        po = obj.po
        stop_reason = 'Shift ended'
        time = timezone.now()
        description = 'The user ' + tech_name + ' ended his shift'
        stop =  Stops(info_id=ID,reason=stop_reason,solution='Not available yet',extra_cause_1='N/A',extra_cause_2='N/A',stop_start_time=time,stop_end_time= time,reason_description=description,po=po)
        stop.save()
        obj.save()
    logout(request)
    messages.success(request, 'You succesfully ended your shift.')
    return HttpResponseRedirect('/admin/')

@login_required()
def Middle(request,action,current_index):
    dict_of_steps = {}
    if 'temp_job_num' in request.session:
        if request.user.is_authenticated() and request.user.is_active:
            job_num = request.session['temp_job_num']
            po = request.session['temp_po']
            pk = request.session['temp_pk']
            job = Info.objects.get(pk = pk)
            features_objects = Features.objects.filter(info_id=job.id,info__po=po,info__Tech_name=request.user.first_name + ' ' + request.user.last_name)
            if job.Tech_name == request.user.first_name + ' ' + request.user.last_name:
                if job.job_type == '2000':
                    dict_of_steps = copy.deepcopy(dict_m2000_new)
                elif job.job_type == '4000':
                    dict_of_steps = copy.deepcopy(dict_m4000_new)
                elif job.job_type == 'ELEM':
                    dict_of_steps = copy.deepcopy(dict_elem_new)
                status = job.status
                list_of_steps = dict_of_steps[status]
                steps_length = job.stage_len
                if job.current_index >= len(list_of_steps):
                    messages.warning(request, 'There seemed to be an error. Try validating the job')
                    return HttpResponseRedirect('/admin/')
                if action == 'next' and ((job.current_index == int(current_index)-1) or job.current_index == 0):
                    if status=='Stopped':
                        return HttpResponseRedirect("/prodfloor/resume/")
                    times = Times.objects.get(info_id=job.id)
                    if remaining_steps(1,job.current_index,dict_of_steps,status,features_objects):
                        dict_of_stages = {1: 'Beginning',
                                          2: 'Program',
                                          3: 'Logic',
                                          4: 'Ending',
                                          5: 'Complete'}
                        for number, stage in dict_of_stages.items():
                            if stage == status:
                                time = timezone.now()
                                if status != 'Complete':
                                    job.status=dict_of_stages[number+1]
                                    job.save()
                                if number==1:
                                    job.prev_stage = 'Beginning'
                                    times.end_time_1 = time
                                    times.start_time_2 = time
                                    job.save()
                                    times.save()
                                elif number==2:
                                    if job.job_type == 'ELEM':
                                        job.prev_stage = 'Program'
                                        job.status = dict_of_stages[number + 2]
                                        times.end_time_2 = time
                                        times.start_time_3 = time
                                        times.end_time_3 = time
                                        times.start_time_4 = time
                                        job.save()
                                        times.save()
                                    else:
                                        job.prev_stage = 'Program'
                                        times.end_time_2 = time
                                        times.start_time_3 = time
                                        job.save()
                                        times.save()
                                elif number==3:
                                    job.prev_stage = 'Logic'
                                    times.end_time_3 = time
                                    times.start_time_4 = time
                                    times.save()
                                elif number==4:
                                    job.prev_stage = 'Ending'
                                    times.end_time_4 = time
                                    times.save()
                                elif number == 5:
                                    job.prev_stage = 'Complete'
                                    job.save()
                                    return redirect("/admin/")
                        status = job.status
                        list_of_steps = dict_of_steps[status]
                        job.stage_len = len(list_of_steps)
                        steps_length = job.stage_len
                        job.current_index = 0
                        while True:
                            current_data = list_of_steps[job.current_index]
                            if compare(current_data[0], current_data[1], current_data[2], features_objects):
                                text = current_data[0]
                                break
                            else:
                                job.current_index += 1
                                job.save()
                        current_step = job.current_index + 1
                        job.save()
                        return render(request, 'prodfloor/newjob.html',{'job_num': job_num, 'job': job, 'steps': steps_length,
                                                                         'current_step_text': text,
                                                                         'current_step': current_step})
                    elif remaining_steps(2,job.current_index,dict_of_steps,status,features_objects):
                        request.session['already_here'] = True
                        job.current_index += 1
                        while True:
                            current_data = list_of_steps[job.current_index]
                            if compare(current_data[0], current_data[1], current_data[2], features_objects):
                                text = current_data[0]
                                break
                            else:
                                job.current_index += 1
                                job.save()
                        current_step = job.current_index + 1
                        job.save()
                        return render(request, 'prodfloor/newjob.html', {'job_num': job_num, 'job': job, 'steps': steps_length,
                                                                         'current_step_text': text,
                                                                         'current_step': current_step,'last':True,'message':_("This was the last step for this stage, you wont be able to return to it once you click OK.")})
                    else:
                        request.session['already_here'] = True
                        job.current_index += 1
                        while True:
                            current_data = list_of_steps[job.current_index]
                            if compare(current_data[0], current_data[1], current_data[2], features_objects):
                                text = current_data[0]
                                break
                            else:
                                job.current_index += 1
                                job.save()
                        current_step = job.current_index + 1
                        job.save()
                        return render(request, 'prodfloor/newjob.html', {'job_num': job_num, 'job': job, 'steps': steps_length,
                                                                     'current_step_text': text,
                                                                     'current_step': current_step})
                elif action == 'back' and (job.current_index == int(current_index)-1) and job.current_index !=0:
                    if job.current_index == 0 and (job.current_index == int(current_index)):
                        if job.job_type == '2000':
                            while True:
                                current_data = list_of_steps[job.current_index]
                                if compare(current_data[0], current_data[1], current_data[2], features_objects):
                                    text = current_data[0]
                                    break
                                else:
                                    job.current_index -= 1
                                    job.save()
                        else:
                            text = list_of_steps[job.current_index]
                        current_step = job.current_index - 1
                        return render(request, 'prodfloor/newjob.html', {'job_num': job_num, 'job': job, 'steps': steps_length,
                                                                         'current_step_text': text,
                                                                         'current_step': current_step})
                    else:
                        request.session['already_here'] = True
                        job.current_index -= 1
                        job.save()
                        while True:
                            current_data = list_of_steps[job.current_index]
                            if compare(current_data[0], current_data[1], current_data[2], features_objects):
                                text = current_data[0]
                                break
                            else:
                                job.current_index -= 1
                                current_index = str(int(current_index)-1)
                                job.save()
                        current_step = int(current_index)-1
                        job.save()
                        return render(request, 'prodfloor/newjob.html', {'job_num': job_num, 'job': job, 'steps': steps_length,
                                                                     'current_step_text': text,
                                                                     'current_step': current_step})
                elif (action == 'next' and (job.current_index == int(current_index))) or (action == 'back' and (((job.current_index == int(current_index))-2) or (job.current_index == 0))):
                        return HttpResponseRedirect("/prodfloor/continue/" + str(pk) + "/" + po)
                elif action == 'back' and (job.current_index == 0):
                    messages.warning(request, 'In order to get to previous stages contact your Administrator.')
                    return HttpResponseRedirect("/prodfloor/continue/" + str(pk) + "/" + po)
                elif action == 'stop':
                    if job.status != 'Stopped':
                        request.session['temp_pk'] = pk
                        request.session['temp_job_num'] = job.job_num
                        request.session['temp_po'] = po
                        return HttpResponseRedirect("/prodfloor/stopped/")
                else:
                    messages.warning(request, 'There seemed to be an error. Try validating the job')
                    return HttpResponseRedirect('/admin/')
            else:
                messages.warning(request, 'The Job you tried to reach is not assigned to you.')
                return HttpResponseRedirect('/admin/')
        else:
            return HttpResponseRedirect('/admin/')
    else:
        messages.warning(request, 'The Job you tried to reach is not available.')
        return HttpResponseRedirect('/admin/')

def done(request):
    return render(request, 'prodfloor/newjob.html')

class Reassign(SessionWizardView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    list = [ReassignJob]

    def get_template_names(self):
        return ["prodfloor/wizard_form_reassign.html"]

    def get_all_cleaned_data(self):
        self.cleaned_data = {}
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            if form_obj.is_valid():
                if isinstance(form_obj.cleaned_data, (tuple, list)):
                    self.cleaned_data.update({
                        'formset-%s' % form_key: form_obj.cleaned_data
                    })
                else:
                    self.cleaned_data.update(form_obj.cleaned_data)

    def done(self, form_list, **kwargs):
        self.get_all_cleaned_data()
        po = kwargs.get('po', None)
        pk  = kwargs.get('pk', None)
        times = Times.objects.get(info__pk=pk)
        time = timezone.now()
        job_num_info = Info.objects.get(pk = pk)
        reason = 'Job reassignment//'
        new_reason = reason + str(self.cleaned_data['reason_description'])
        new_tech_obj = self.cleaned_data['new_tech']
        new_tech = new_tech_obj.first_name + ' ' + new_tech_obj.last_name
        station = self.cleaned_data['station']
        description = 'Job # '+ job_num_info.job_num + ' reassigned to ' + new_tech
        if job_num_info.status != 'Stopped':
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
        job_num_info.status = 'Complete'
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
        job_num_stop = Stops(info_id=ID,reason=new_reason,extra_cause_1='N/A',extra_cause_2='N/A',solution='Not available yet',stop_start_time=time,stop_end_time= time,reason_description=description, po=po)
        job_num_stop.save()
        messages.success(self.request,'The Job ' + job_num_info.job_num + ' has been properly reassigned.')
        return HttpResponseRedirect("/admin/prodfloor/myjob/"+str(job_num_info.id)+"/change/")

def first(request):
    job = Info.objects.filter(Tech_name=request.user.first_name + ' ' + request.user.last_name).exclude(
        status='Complete').exclude(status='Stopped')
    c=0
    for object in job:
        c+=1
    if c>0:
        messages.warning(request,'You already have one active Job. In order to create a new one stop or finish the active one.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect("/prodfloor/job/")

class JobInfo(SessionWizardView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    jobs_list=[Maininfo,FeaturesSelection]

    def get_template_names(self):
        if self.steps.current == '0':
            return ['formtools/wizard/wizard_form.html']
        elif self.steps.current == '1':
            return ['prodfloor/wizard_form.html']
        else:
            return ['prodfloor/wizard_form.html']

    def get_all_cleaned_data(self):
        self.cleaned_data = {}
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            if form_obj.is_valid():
                if isinstance(form_obj.cleaned_data, (tuple, list)):
                    self.cleaned_data.update({
                        'formset-%s' % form_key: form_obj.cleaned_data
                    })
                else:
                    self.cleaned_data.update(form_obj.cleaned_data)

    def done(self, form_list, **kwargs):
        previous_jobs = Info.objects.all()
        self.get_all_cleaned_data()
        if self.request.user.is_authenticated() and self.request.user.is_active:
            self.request.session['pp_jobinfo'] = True
        user_name = self.request.user.first_name
        user_lastname = self.request.user.last_name
        job_num = str(self.cleaned_data['job_num'])
        Tech_name = user_name + ' ' + user_lastname
        ship_date = self.cleaned_data['ship_date']
        job_type = self.cleaned_data['job_type']
        PO = str(self.cleaned_data['po'])
        label = self.cleaned_data['label']
        station = self.cleaned_data['station']
        status = 'Beginning'
        if any(PO in obj.po for obj in previous_jobs ):
            messages.warning(self.request,'The Job# ' + job_num + ' with PO# '+ PO + ' has already been created. If needed, request the administrator for a reassignment.')
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        job_info_new_row=Info(job_num=job_num,Tech_name=Tech_name,status=status,ship_date=ship_date,current_index=0,job_type=job_type,stage_len=99,po=PO,label=label,station=station)
        job_info_new_row.save()
        ID=job_info_new_row.id
        features=self.cleaned_data['features_selection']
        if any(obj == 'None' for obj in features):
            pass
        else:
            for obj in features:
                job_features_new_row=Features(info_id=ID,features=obj)
                job_features_new_row.save()
        self.request.session['temp_job_num']= job_num
        self.request.session['temp_po'] = PO
        self.request.session['temp_pk'] =job_info_new_row.pk
        creation_time = timezone.now()
        start_time=Times(info_id=ID,start_time_1=creation_time,end_time_1=creation_time,start_time_2=creation_time,end_time_2=creation_time,start_time_3=creation_time,end_time_3=creation_time,start_time_4=creation_time,end_time_4=creation_time)
        start_time.save()
        return HttpResponseRedirect("/prodfloor/start/")

class Stop(SessionWizardView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    form_list=[StopReason]

    def get_template_names(self):
        return ["prodfloor/wizard_form_stop.html"]

    def get_all_cleaned_data(self):
        self.cleaned_data = {}
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            if form_obj.is_valid():
                if isinstance(form_obj.cleaned_data, (tuple, list)):
                    self.cleaned_data.update({
                        'formset-%s' % form_key: form_obj.cleaned_data
                    })
                else:
                    self.cleaned_data.update(form_obj.cleaned_data)

    def done(self, form_list, **kwargs):
        if self.request.user.is_authenticated() and self.request.user.is_active:
            job_num = self.request.session['temp_job_num']
            po = self.request.session['temp_po']
            pk = self.request.session['temp_pk']
            job = Info.objects.get(pk=pk)
            ID = job.id
            self.get_all_cleaned_data()
            stop_reason=self.cleaned_data['reason_for_stop']
            description = self.cleaned_data['reason_description']
            time = timezone.now()
            stop = Stops(info_id=ID,reason=stop_reason,extra_cause_1='N/A',extra_cause_2='N/A',solution='Not available yet',stop_start_time=time,stop_end_time= time,reason_description=description,po=po)
            if job.status != 'Stopped':
                job.prev_stage = job.status
            job.status = 'Stopped'
            job.save()
            stop.save()
            return HttpResponseRedirect("/prodfloor/continue/"+str(pk)+"/" + po)

class SuperUserStop(SessionWizardView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    form_list=[StopReason]

    def get_template_names(self):
        return ["prodfloor/wizard_form_stop.html"]

    def get_all_cleaned_data(self):
        self.cleaned_data = {}
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            if form_obj.is_valid():
                if isinstance(form_obj.cleaned_data, (tuple, list)):
                    self.cleaned_data.update({
                        'formset-%s' % form_key: form_obj.cleaned_data
                    })
                else:
                    self.cleaned_data.update(form_obj.cleaned_data)

    def done(self, form_list, **kwargs):
        if self.request.user.is_authenticated() and self.request.user.is_active:
            job_num = self.request.session['temp_job_num']
            po = self.request.session['temp_po']
            job = Info.objects.exclude(status = 'Complete').get(job_num=job_num,po=po)
            ID = job.id
            self.get_all_cleaned_data()
            stop_reason=self.cleaned_data['reason_for_stop']
            description = self.cleaned_data['reason_description']
            time = timezone.now()
            stop = Stops(info_id=ID,reason=stop_reason,extra_cause_1='N/A',extra_cause_2='N/A',solution='Not available yet',stop_start_time=time,stop_end_time= time,reason_description=description,po=po)
            if job.status != 'Stopped':
                job.prev_stage = job.status
            job.status = 'Stopped'
            job.save()
            stop.save()
            messages.warning(self.request, _('The Stop has been properly registered.'))
            return HttpResponseRedirect('/admin/')

class ResumeView(SessionWizardView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    form_list=[ResumeSolution]

    def get_template_names(self):
        return ["prodfloor/wizard_form_resume.html"]

    def get_form_initial(self, step):
        initial = {}
        po = self.request.session['temp_po']
        job_num = self.request.session['temp_job_num']
        pk = self.request.session['temp_pk']
        job = Info.objects.get(pk = pk)
        ID = job.id
        stop = Stops.objects.get(info_id=ID, solution='Not available yet', po=po)
        tier1 = stop.reason
        reason_id = Tier1.objects.get(tier_one_cause=tier1)
        initial.update({'tier1':tier1})
        return self.initial_dict.get(step, initial)

    def get_all_cleaned_data(self):
        self.cleaned_data = {}
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            if form_obj.is_valid():
                if isinstance(form_obj.cleaned_data, (tuple, list)):
                    self.cleaned_data.update({
                        'formset-%s' % form_key: form_obj.cleaned_data
                    })
                else:
                    self.cleaned_data.update(form_obj.cleaned_data)

    def done(self, form_list, **kwargs):
        if self.request.user.is_authenticated() and self.request.user.is_active:
            job_num = self.request.session['temp_job_num']
            po = self.request.session['temp_po']
            pk = self.request.session['temp_pk']
            job = Info.objects.get(pk = pk)
            job.status = job.prev_stage
            job.prev_stage = 'Stopped'
            ID = job.id
            self.get_all_cleaned_data()
            solution=self.cleaned_data['solution']
            cause_1 = self.cleaned_data['tier2']
            cause_2 = self.cleaned_data['tier3']
            stop = Stops.objects.get(info_id=ID,solution='Not available yet',po=po)
            stop.solution = solution
            stop.extra_cause_1 =cause_1
            stop.extra_cause_2 = cause_2
            stop.stop_end_time = timezone.now()
            job.save()
            stop.save()
            return HttpResponseRedirect("/prodfloor/continue/" + str(pk) + "/" + po)

def get_tier_2(request):
    if request.method == 'POST':
        tier1 = request.POST.get('tier1')
        tier_two_causes={0:'------'}
        tier2 = Tier2.objects.filter(tier_one__tier_one_cause=tier1)
        if tier2.count()<=0:
            tier_two_causes[0]='N/A'
        else:
            for obj in tier2:
                tier_two_causes[obj.id]=obj.tier_two_cause
        return HttpResponse(json.dumps(tier_two_causes),content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def get_tier_3(request):
    if request.method == 'POST':
        tier1 = request.POST.get('tier1')
        tier2 = request.POST.get('tier2')
        tier_three_causes = {}
        reason_id = Tier1.objects.get(tier_one_cause=tier1)
        tier3 = Tier3.objects.filter(tier_two__tier_two_cause=tier2,tier_two__tier_one_id=reason_id.id)
        if tier3.count()<=0:
            tier_three_causes[0] = 'N/A'
        else:
            for obj in tier3:
                tier_three_causes[obj.id]=obj.tier_three_cause

        return HttpResponse(json.dumps(tier_three_causes),content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def get_stations(request):
    if request.method == 'POST':
        job_type = request.POST.get('job_type')
        dict = stations_by_type
        if job_type == '0':
            stations = {'0':'-----'}
        else:
            stations = dict[job_type]

        return HttpResponse(json.dumps(stations),content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def createStop(request):
    if request.method == 'POST':#this if is for the filtering, the arguments to filter are received through it
        form = SUStop(request.POST)
        if form.is_valid():
            request.session['temp_job_num'] = form.cleaned_data['job_num']
            request.session['temp_po'] = form.cleaned_data['po']
            return HttpResponseRedirect('/prodfloor/su/stop/')
        else:
            return render(request, 'prodfloor/su_report_stop.html', {'form': form})
    else:
        form = SUStop
        return render(request, 'prodfloor/su_report_stop.html', {'form': form})

def multiplereassigns(request):
    QuestionFormSet = formset_factory(MultipleReassign,extra=0)
    if request.method == "POST":
        formset = QuestionFormSet(request.POST)
        if(formset.is_valid()):
            for form in formset:
                update = form.cleaned_data['tobeupdated']
                if update:
                    job_num = form.cleaned_data['job_num']
                    po = form.cleaned_data['po']
                    pk = Info.objects.exclude(status="Complete").get(po=po).pk
                    tech = form.cleaned_data['new_tech']
                    station = form.cleaned_data['station']
                    reason = form.cleaned_data['reason_description']
                    new_values_dict = {"new_tech":tech,"station":station,"reason":reason,"job_num":job_num}
                    multireassignfunct(pk,new_values_dict)
            messages.success(request, 'The Jobs selected have been succesfully reassigned.')
            return HttpResponseRedirect('/prodfloor/su/multiple_reassign')
            #for form in formset:
            #    print("Cool")
        else:
            print("NOT Cool")
            new_formset = []
            for form in formset:
                print(form.cleaned_data)
                #job_num = form.cleaned_data['job_num']
                #po = form.cleaned_data['po']
                #tech = form.cleaned_data['new_tech']
                #station = form.cleaned_data['station']
                #reason = form.cleaned_data['reason_description']
                #new_formset.append({"job_num": job_num, "po": po, "new_tech": tech, "station": station,"reason_description":reason})
            return render(request, 'prodfloor/MUreassign.html', {'formset': formset,'headers':mureassign_headers})
    else:
        jobs = Info.objects.exclude(status="Complete")
        initial = []
        for job in jobs:
            full_name = job.Tech_name.split(' ',)
            name = full_name[0]
            last_name = full_name[1]
            initial.append({"job_num":job.job_num,"po":job.po,"new_tech":User.objects.get(first_name=name,last_name=last_name).pk,"station":job.station})
        return render(request,'prodfloor/MUreassign.html',{'formset': QuestionFormSet(initial = initial),'headers':mureassign_headers})