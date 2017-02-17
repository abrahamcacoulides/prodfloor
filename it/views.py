from django.http import Http404, HttpResponseRedirect,HttpResponse
from formtools.wizard.views import SessionWizardView
from .models import IT_model
from django.contrib import messages
import json
from .forms import MyModelForm
from django.utils import timezone

def Temp(request):
    messages.warning(request, 'This Feature is not available yet. Please use this view to fill the information')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ServerStop(SessionWizardView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    form_list=[MyModelForm]

    def get_template_names(self):
        return ["it/wizard_form_it.html"]

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

    def get_form_initial(self, step,**kwargs):
        id_passed = kwargs.get('number', None)
        print(id_passed)
        server_stop = IT_model.objects.get(pk=id_passed)
        initial = {}
        issue = server_stop.issue
        status = server_stop.status
        initial.update({'issue':issue,'status':status})
        return self.initial_dict.get(step, initial)

    def done(self,**kwargs):
        if self.request.user.is_authenticated() and self.request.user.is_active:
            id = kwargs.get('id',None)
            #server_stop = IT_model.objects.get(id=id)
            data=self.get_all_cleaned_data()
            print(data)
            #server_stop.cause = self.cleaned_data['cause']
            #server_stop.status = self.cleaned_data['status']
            #server_stop.solution = self.cleaned_data['solution']
            #server_stop.end_time = self.cleaned_data['end']
            #server_stop.save()
            return HttpResponseRedirect("/admin/")