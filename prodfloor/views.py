from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from formtools.wizard.views import SessionWizardView
from prodfloor.forms import Maininfo, FeaturesSelection, StopReason, ResumeSolution
from prodfloor.models import Info,Features,Times, Stops
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Info

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

def detail(request, info_job_num):
    try:
        job = Info.objects.get(job_num=info_job_num)
    except Info.DoesNotExist:
        raise Http404("Job doesnt exist")
    return render(request, 'prodfloor/detail.html', {'job': job})

@login_required()
def Start(request):
    if 'pp_jobinfo' in request.session:
        dict_of_steps = {'Beginning':['Documentacion Inicial',
                                      'Inspeccion Visual',
                                      'Preparacion de Labview',
                                      'Chequeo preliminar de voltajes iniciales'],
                         'Program':['Programacion de Flasheo',
                                    'Programacion del Firmware',
                                    'Programacion del Solid State Starter',
                                    'Programacion de paramtros F1',
                                    'Programacion tarjeta CE Electronics'],
                         'Logic':['Board power test SAFL & SAFS',
                                  'Motor Starter Test',
                                  'Valve control and limits',
                                  'Safety and inspection',
                                  'Door locks and hoistway access',
                                  'Landing system',
                                  'Door Interface',
                                  'COP parte 1',
                                  'Fire Service Phase I',
                                  'Fire Service Phase II',
                                  'Movement Indication',
                                  'Calls',
                                  'Programmable Input/Outputs'],
                         'Ending':['Inspeccion Final',
                                   'Passcode',
                                   'Papeleria Final',
                                   'Respaldo Electronico de la papeleria',
                                   'Desconnecion de Arneces',
                                   'Carro a estacion final'],
                         'Complete':['Fin de pruebas']}
        job_num = request.session['temp_job_num']
        job = Info.objects.get(job_num=job_num)
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
def Continue(request,jobnum):
    if request.user.is_authenticated() and request.user.is_active:
        request.session['temp_job_num']=jobnum
        dict_of_steps = {
            'Beginning' : ['Documentacion Inicial',
                          'Inspeccion Visual',
                          'Preparacion de Labview',
                          'Chequeo preliminar de voltajes iniciales'],
            'Program' : ['Programacion de Flasheo',
                        'Programacion del Firmware',
                        'Programacion del Solid State Starter',
                        'Programacion de paramtros F1',
                        'Programacion tarjeta CE Electronics'],
            'Logic' : ['Board power test SAFL & SAFS',
                      'Motor Starter Test',
                      'Valve control and limits',
                      'Safety and inspection',
                      'Door locks and hoistway access',
                      'Landing system',
                      'Door Interface',
                      'COP parte 1',
                      'Fire Service Phase I',
                      'Fire Service Phase II',
                      'Movement Indication',
                      'Calls',
                      'Programmable Input/Outputs'],
            'Ending' : ['Inspeccion Final',
                       'Passcode',
                       'Papeleria Final',
                       'Respaldo Electronico de la papeleria',
                       'Desconnecion de Arneces',
                       'Carro a estacion final'],
            'Complete' : ['Fin de pruebas'],
            'Stopped' : ["Detenido"]}
        job_num=jobnum
        job = Info.objects.get(job_num=job_num)
        status = job.status
        list_of_steps = dict_of_steps[status]
        index_num = job.current_index
        steps_length = len(list_of_steps)
        current_step = index_num + 1
        if job.status == 'Stopped':
            index_num = 0
            current_step = index_num + 1
            return render(request, 'prodfloor/continuejob.html', {'job_num': job_num, 'job': job, 'steps': steps_length,
                                                                  'current_step_text': list_of_steps[index_num],
                                                                  'current_step': current_step})
        else:
            return render(request, 'prodfloor/continuejob.html', {'job_num': job_num, 'job': job, 'steps': steps_length,
                                                         'current_step_text': list_of_steps[index_num],
                                                         'current_step': current_step})


@login_required()
def Middle(request,action):
    if request.user.is_authenticated() and request.user.is_active:
        dict_of_steps = {
            'Beginning': ['Documentacion Inicial',
                                       'Inspeccion Visual',
                                       'Preparacion de Labview',
                                       'Chequeo preliminar de voltajes iniciales'],
                         'Program': ['Programacion de Flasheo',
                                     'Programacion del Firmware',
                                     'Programacion del Solid State Starter',
                                     'Programacion de paramtros F1',
                                     'Programacion tarjeta CE Electronics'],
                         'Logic': ['Board power test SAFL & SAFS',
                                   'Motor Starter Test',
                                   'Valve control and limits',
                                   'Safety and inspection',
                                   'Door locks and hoistway access',
                                   'Landing system',
                                   'Door Interface',
                                   'COP parte 1',
                                   'Fire Service Phase I',
                                   'Fire Service Phase II',
                                   'Movement Indication',
                                   'Calls',
                                   'Programmable Input/Outputs'],
                         'Ending': ['Inspeccion Final',
                                    'Passcode',
                                    'Papeleria Final',
                                    'Respaldo Electronico de la papeleria',
                                    'Desconnecion de Arneces',
                                    'Carro a estacion final'],
                         'Complete': ['Fin de pruebas'],
                        'Stopped': ['Detenido']}
        job_num = request.session['temp_job_num']
        job = Info.objects.get(job_num=job_num)
        status = job.status
        list_of_steps = dict_of_steps[status]
        steps_length = job.stage_len
        index_num = job.current_index
        if action == 'next':
            if status=='Stopped':
                return HttpResponseRedirect("http://127.0.0.1:8000/prodfloor/resume/")
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
                            return redirect(r'http://127.0.0.1:8000/prodfloor')
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
        elif action == 'back':
            if index_num == 0:
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
        elif action == 'stop':
            if job.status != 'Stopped':
                job.prev_stage = job.status
                job.status='Stopped'
                job.save()
                return HttpResponseRedirect("http://127.0.0.1:8000/prodfloor/stop/")
            else:
                pass
        else:
            raise Http404("This is not the droid you're looking for")
    else:
        raise Http404("This is not the droid you're looking for")


def done(request):
    return render(request, 'prodfloor/newjob.html')

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
        if self.request.user.is_authenticated() and self.request.user.is_active:
            self.request.session['pp_jobinfo'] = True
        user_id = self.request.user.id
        user_name = self.request.user.first_name
        user_lastname = self.request.user.last_name
        self.get_all_cleaned_data()
        job_num=self.cleaned_data['job_num']
        Tech_name=user_name + ' ' + user_lastname
        ship_date=self.cleaned_data['ship_date']
        job_type = self.cleaned_data['job_type']
        status='Beginning'
        job_info_new_row=Info(job_num=job_num,Tech_name=Tech_name,status=status,ship_date=ship_date,current_index=0,job_type=job_type,stage_len=99)
        job_info_new_row.save()
        ID=job_info_new_row.id
        features=self.cleaned_data['features_selection']
        for obj in features:
            job_features_new_row=Features(info_id=ID,features=obj)
            job_features_new_row.save()
        self.request.session['temp_job_num']=job_num
        creation_time = timezone.now()
        start_time=Times(info_id=ID,start_time_1=creation_time,end_time_1=creation_time,start_time_2=creation_time,end_time_2=creation_time,start_time_3=creation_time,end_time_3=creation_time,start_time_4=creation_time,end_time_4=creation_time)
        start_time.save()
        return HttpResponseRedirect("http://127.0.0.1:8000/prodfloor/end/")


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
            job = Info.objects.get(job_num=job_num)
            ID = job.id
            self.get_all_cleaned_data()
            stop_reason=self.cleaned_data['reason_for_stop']
            time = timezone.now()
            stop = Stops(info_id=ID,reason=stop_reason,solution='Not available yet',stop_start_time=time,stop_end_time= time)
            job.save()
            stop.save()
            return HttpResponseRedirect("http://127.0.0.1:8000/prodfloor/continue/"+job_num)


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
            job = Info.objects.get(job_num=job_num)
            job.status = job.prev_stage
            job.prev_stage = 'Stopped'
            ID = job.id
            self.get_all_cleaned_data()
            solution=self.cleaned_data['solution']
            stop = Stops.objects.get(info_id=ID,solution='Not available yet')
            stop.solution = solution
            stop.stop_end_time = timezone.now()
            job.save()
            stop.save()
            return HttpResponseRedirect("http://127.0.0.1:8000/prodfloor/continue/" + job_num)