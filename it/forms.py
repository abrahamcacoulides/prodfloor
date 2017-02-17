from django import forms
from django.utils import timezone
from .models import ServerCauses

class MyModelForm(forms.Form):
    initial = timezone.datetime.today
    issue = forms.CharField(max_length=100, label='Issue',widget=forms.TextInput(attrs = {'readonly':True,'onclick':'console.log(this)'}))
    cause = forms.ModelChoiceField(queryset=ServerCauses.objects.all(),label='Main Cause:')
    status = forms.ChoiceField(choices=(('On Going','On Going'),('Pending','Pending'),('Complete','Complete')),label='Status')
    solution = forms.CharField(required=True, widget=forms.Textarea,label='Solution')
    end = forms.DateField(label='End date',widget = forms.SelectDateWidget, input_formats=['%Y-%m-%d'], initial= initial)