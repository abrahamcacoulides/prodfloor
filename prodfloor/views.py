from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView
from prodfloor.forms import Maininfo, FeaturesSelection, StopReason, ResumeSolution, ReassignJob, getTechs
from django.contrib.auth import logout
from prodfloor.models import Info,Features,Times, Stops
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from prodfloor.dicts import dict_elem,dict_m2000,dict_m4000

def prodfloor_view(request):
    job_list = Info.objects.order_by('job_num')
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

def detail(request, info_job_num):#TODO is this view really needed? right now is only showing some things about the job *maybe I can develop it a bit more
    try:
        job = Info.objects.get(job_num=info_job_num)
    except Info.DoesNotExist:
        raise Http404("Job doesnt exist")
    return render(request, 'prodfloor/detail.html', {'job': job})

@login_required()
def Start(request):
    if 'pp_jobinfo' in request.session:
        dict_of_steps = {}#TODO how to change the dictionary depending on the features of the job? should it be stored in the DB or can it be done per session?
        job_num = request.session['temp_job_num']
        po = request.session['temp_po']
        job = Info.objects.get(job_num=job_num,po=po,Tech_name=request.user.first_name + ' ' + request.user.last_name)
        if job.job_type == '2000':
            dict_of_steps = dict_m2000
        elif job.job_type == '4000':
            dict_of_steps = dict_m4000
        elif job.job_type == 'ELEM':
            dict_of_steps = dict_elem
        status = job.status
        list_of_steps = dict_of_steps[status]
        job.stage_len = len(list_of_steps)
        steps_length = job.stage_len
        request.session['already_here'] = True
        job.current_index = 0
        index_num = job.current_index
        current_step = index_num + 1
        job.save()
        del request.session['pp_jobinfo']
        return render(request, 'prodfloor/newjob.html', {'job_num': job_num, 'job': job, 'steps': steps_length,
                                                         'current_step_text': list_of_steps[index_num],
                                                         'current_step': current_step})
    else:
        raise Http404("This is not the droid you're looking for")

@login_required()
def Continue(request,jobnum,po):
    if request.user.is_authenticated() and request.user.is_active:
        request.session['temp_job_num']=jobnum
        request.session['temp_po'] = po
        dict_of_steps = {}#TODO how to change the dictionary depending on the features of the job? should it be stored in the DB or can it be done per session?
        job_num=jobnum
        job = Info.objects.get(job_num=job_num,po=po)
        if job.job_type == '2000':
            dict_of_steps = dict_m2000
        elif job.job_type == '4000':
            dict_of_steps = dict_m4000
        elif job.job_type == 'ELEM':
            dict_of_steps = dict_elem
        status = job.status
        list_of_steps = dict_of_steps[status]
        index_num = job.current_index
        steps_length = len(list_of_steps)
        job.stage_len = steps_length
        job.save()
        current_step = index_num + 1
        if  job.Tech_name == request.user.first_name + ' ' + request.user.last_name:
            if job.status == 'Stopped':
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
                                index_num = job.current_index
                                current_step = index_num + 1
                                return render(request, 'prodfloor/newjob.html',{'job_num': job_num, 'job': job, 'steps': steps_length,'current_step_text': list_of_steps[index_num], 'current_step': current_step})
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
                        index_num = job.current_index
                        current_step = index_num+1
                        return render(request, 'prodfloor/newjob.html',{'job_num': job_num, 'job': job, 'steps': steps_length,
                                       'current_step_text': list_of_steps[index_num], 'current_step': current_step})
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
                        index_num = job.current_index
                        current_step = index_num + 1
                        return render(request, 'prodfloor/newjob.html',{'job_num': job_num, 'job': job, 'steps': steps_length,'current_step_text': list_of_steps[index_num],'current_step': current_step})
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
                                                         'current_step_text': list_of_steps[index_num],
                                                         'current_step': current_step})
        else:
            messages.warning(request, 'This Job is assigned to someone else.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
        stop =  Stops(info_id=ID,reason=stop_reason,solution='Not available yet',stop_start_time=time,stop_end_time= time,reason_description=description,po=po)
        stop.save()
        obj.save()
    logout(request)
    messages.success(request, 'You succesfully ended your shift.')
    return HttpResponseRedirect('/admin/')


@login_required()
def Middle(request,action,index):
    if request.user.is_authenticated() and request.user.is_active:
        dict_of_steps = {}#TODO how to change the dictionary depending on the features of the job? should it be stored in the DB or can it be done per session?
        job_num = request.session['temp_job_num']
        po = request.session['temp_po']
        job = Info.objects.get(job_num=job_num,po=po)
        features_objects = Features.objects.filter(info_id=job.id,info__po=po)
        if job.job_type == '2000':
            dict_of_steps = dict_m2000
            if any(feature.features == 'COP' for feature in features_objects):
                if 'Conexion de arneces del simulador' in dict_of_steps['Program']:
                    index = dict_of_steps['Program'].index('Conexion de arneces del simulador')
                    dict_of_steps['Program'].pop(index)
            else:
                if 'Conexion de arneces simulador del carro y arneceses cartop' in dict_of_steps['Program']:
                    index = dict_of_steps['Program'].index('Conexion de arneces simulador del carro y arneceses cartop')
                    dict_of_steps['Program'].pop(index)
            if any(feature.features == 'SHC' for feature in features_objects):
                pass
            else:
                if 'Serial Hall Calls (Pag SH)' in dict_of_steps['Logic']:
                    index = dict_of_steps['Logic'].index('Serial Hall Calls (Pag SH)')
                    dict_of_steps['Logic'].pop(index)
            if any(feature.features == 'DCC' for feature in features_objects):
                if 'Door Interface (Pag 11, 11X)' in dict_of_steps['Logic']:
                    index = dict_of_steps['Logic'].index('Door Interface (Pag 11, 11X)')
                    dict_of_steps['Logic'].pop(index)
            else:
                if 'Door Interface (Pag CT1, CT2)' in dict_of_steps['Logic']:
                    index = dict_of_steps['Logic'].index('Door Interface (Pag CT1, CT2)')
                    dict_of_steps['Logic'].pop(index)
                    dict_of_steps['Logic'].pop(index)
            if any(feature.features == 'CPI' for feature in features_objects):
                if 'Fire Service Phase II (Pag 12)' in dict_of_steps['Logic']:
                    index = dict_of_steps['Logic'].index('Fire Service Phase II (Pag 12)')
                    dict_of_steps['Logic'].pop(index)
                    dict_of_steps['Logic'].pop(index)
            else:
                if 'Fire Service Phase II (Pag CPI)' in dict_of_steps['Logic']:
                    index = dict_of_steps['Logic'].index('Fire Service Phase II (Pag CPI)')
                    dict_of_steps['Logic'].pop(index)
                    dict_of_steps['Logic'].pop(index)
                    dict_of_steps['Logic'].pop(index)
        elif job.job_type == '4000':
            dict_of_steps = dict_m4000
            if any(feature.features == 'COP' for feature in features_objects):
                if 'Conexion de arneces del simulador' in dict_of_steps['Program']:
                    index = dict_of_steps['Program'].index('Conexion de arneces del simulador')
                    dict_of_steps['Program'].pop(index)
            else:
                if 'Conexion de arneces simulador del carro y arneceses cartop' in dict_of_steps['Program']:
                    index = dict_of_steps['Program'].index('Conexion de arneces simulador del carro y arneceses cartop')
                    dict_of_steps['Program'].pop(index)
            if any(feature.features == 'SHC' for feature in features_objects):
                pass
            else:
                if 'Serial Hall Calls (Pag SH)' in dict_of_steps['Logic']:
                    index = dict_of_steps['Logic'].index('Serial Hall Calls (Pag SH)')
                    dict_of_steps['Logic'].pop(index)
            if any(feature.features == 'DCC' for feature in features_objects):
                if 'Door Interface (Pag 11, 11X)' in dict_of_steps['Logic']:
                    index = dict_of_steps['Logic'].index('Door Interface (Pag 11, 11X)')
                    dict_of_steps['Logic'].pop(index)
            else:
                if 'Door Interface (Pag CT1, CT2)' in dict_of_steps['Logic']:
                    index = dict_of_steps['Logic'].index('Door Interface (Pag CT1, CT2)')
                    dict_of_steps['Logic'].pop(index)
                    dict_of_steps['Logic'].pop(index)
            if any(feature.features == 'CPI' for feature in features_objects):
                if 'Fire Service Phase II (Pag 12)' in dict_of_steps['Logic']:
                    index = dict_of_steps['Logic'].index('Fire Service Phase II (Pag 12)')
                    dict_of_steps['Logic'].pop(index)
                    dict_of_steps['Logic'].pop(index)
            else:
                if 'Fire Service Phase II (Pag CPI)' in dict_of_steps['Logic']:
                    index = dict_of_steps['Logic'].index('Fire Service Phase II (Pag CPI)')
                    dict_of_steps['Logic'].pop(index)
                    dict_of_steps['Logic'].pop(index)
                    dict_of_steps['Logic'].pop(index)
        elif job.job_type == 'ELEM':
            dict_of_steps = dict_elem
            if any(feature.features == 'HAPS' for feature in features_objects):
                pass
            else:
                if dict_of_steps['Program'][0] == 'Flashear HAPS':
                    dict_of_steps['Program'].pop(0)
        status = job.status
        list_of_steps = dict_of_steps[status]
        steps_length = job.stage_len
        index_num = job.current_index
        if action == 'next' and ((index_num == int(index)-1) or index_num == 0):
            if status=='Stopped':
                return HttpResponseRedirect("/prodfloor/resume/")
            times = Times.objects.get(info_id=job.id)
            if index_num+1 == steps_length:
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
                index_num = job.current_index
                current_step = index_num + 1
                job.save()
                return render(request, 'prodfloor/newjob.html',{'job_num': job_num, 'job': job, 'steps': steps_length,
                                                                 'current_step_text': list_of_steps[index_num],
                                                                 'current_step': current_step,'last':True,'message':'You wont be able to return'})
            else:
                request.session['already_here'] = True
                job.current_index += 1
                index_num=job.current_index
                current_step = index_num + 1
                job.save()
                return render(request, 'prodfloor/newjob.html', {'job_num': job_num, 'job': job, 'steps': steps_length,
                                                             'current_step_text': list_of_steps[index_num],
                                                             'current_step': current_step})
        elif action == 'back' and (index_num == int(index)-1) and index_num !=0:
            if index_num == 0 and (index_num == int(index)):
                current_step = index_num + 1
                return render(request, 'prodfloor/newjob.html', {'job_num': job_num, 'job': job, 'steps': steps_length,
                                                                 'current_step_text': list_of_steps[index_num],
                                                                 'current_step': current_step})
            else:
                request.session['already_here'] = True
                job.current_index -= 1
                index_num = job.current_index
                current_step = index_num + 1
                job.save()
                return render(request, 'prodfloor/newjob.html', {'job_num': job_num, 'job': job, 'steps': steps_length,
                                                             'current_step_text': list_of_steps[index_num],
                                                             'current_step': current_step})
        elif (action == 'next' and (index_num == int(index))) or (action == 'back' and (((index_num == int(index))-2) or (index_num == 0))):
            return HttpResponseRedirect("/prodfloor/continue/" + job_num)
        elif action == 'stop':
            if job.status != 'Stopped':
                return HttpResponseRedirect("/prodfloor/stopped/")
        else:
            raise Http404("This is not the droid you're looking for")
    else:
        raise Http404("This is not the droid you're looking for")


def done(request):
    return render(request, 'prodfloor/newjob.html')

class Reassign(SessionWizardView):
    getTechs()
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    list = [ReassignJob]
    #template_name = 'testwebpage/prodfloor/templates/formtools/wizard/reassign.html'

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
        self.jobnum = kwargs.get('jobnum', None)
        po = kwargs.get('po', None)
        time = timezone.now()
        job_num_info = Info.objects.get(job_num=self.jobnum, po=po)
        reason = 'Job reassignment'
        new_tech = self.cleaned_data['new_tech']
        station = self.cleaned_data['station']
        description = 'Job # '+ job_num_info.job_num + ' reassigned to ' + new_tech
        ID = job_num_info.id
        job_num_info.Tech_name = new_tech
        job_num_info.station = station
        if job_num_info.status != 'Stopped':
            job_num_info.prev_stage = job_num_info.status
        job_num_info.status = 'Stopped'
        job_num_info.save()
        job_num_stop = Stops(info_id=ID,reason=reason,solution='Not available yet',stop_start_time=time,stop_end_time= time,reason_description=description, po=po)
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
        job_num = self.cleaned_data['job_num']
        Tech_name = user_name + ' ' + user_lastname
        ship_date = self.cleaned_data['ship_date']
        job_type = self.cleaned_data['job_type']
        PO = self.cleaned_data['po']
        label = self.cleaned_data['label']
        station = self.cleaned_data['station']
        status = 'Beginning'
        if any(self.cleaned_data['po'] in obj.po for obj in previous_jobs ):
            messages.warning(self.request,'The Job# ' + job_num + ' with PO# '+ PO + ' has already been created. If needed, request the administrator for a reassignment.')
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        job_info_new_row=Info(job_num=job_num,Tech_name=Tech_name,status=status,ship_date=ship_date,current_index=0,job_type=job_type,stage_len=99,po=PO,label=label,station=station)
        job_info_new_row.save()
        ID=job_info_new_row.id
        features=self.cleaned_data['features_selection']
        for obj in features:
            job_features_new_row=Features(info_id=ID,features=obj)
            job_features_new_row.save()
        self.request.session['temp_job_num']= job_num
        self.request.session['temp_po'] = PO
        creation_time = timezone.now()
        start_time=Times(info_id=ID,start_time_1=creation_time,end_time_1=creation_time,start_time_2=creation_time,end_time_2=creation_time,start_time_3=creation_time,end_time_3=creation_time,start_time_4=creation_time,end_time_4=creation_time, po=PO)
        start_time.save()
        return HttpResponseRedirect("/prodfloor/start/")


class Stop(SessionWizardView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    form_list=[StopReason]
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
            job = Info.objects.get(job_num=job_num,po=po)
            ID = job.id
            self.get_all_cleaned_data()
            stop_reason=self.cleaned_data['reason_for_stop']
            description = self.cleaned_data['reason_description']
            time = timezone.now()
            stop = Stops(info_id=ID,reason=stop_reason,solution='Not available yet',stop_start_time=time,stop_end_time= time,reason_description=description,po=po)
            if job.status != 'Stopped':
                job.prev_stage = job.status
            job.status = 'Stopped'
            job.save()
            stop.save()
            return HttpResponseRedirect("/prodfloor/continue/"+job_num+"/" + po)


class ResumeView(SessionWizardView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    form_list=[ResumeSolution]
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
            job = Info.objects.get(job_num=job_num,po=po)
            job.status = job.prev_stage
            job.prev_stage = 'Stopped'
            ID = job.id
            self.get_all_cleaned_data()
            solution=self.cleaned_data['solution']
            stop = Stops.objects.get(info_id=ID,solution='Not available yet',po=po)
            stop.solution = solution
            stop.stop_end_time = timezone.now()
            job.save()
            stop.save()
            return HttpResponseRedirect("/prodfloor/continue/" + job_num + "/" + po)