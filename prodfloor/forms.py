from django import forms
from django.utils import timezone
import datetime

techs_list=((1,"Technician One"),(2,"Technician Two"))
features=(('COP','Car Operating Panel'),('HAPS','HAPS battery'),('SHC','Serial Hall Calls'))

class Maininfo(forms.Form):
    initial = timezone.datetime.today
    job_num = forms.CharField(max_length=10, label='Job #')
    job_type = forms.ChoiceField(label='Job type', choices=(('2000', 'M2000'), ('4000', 'M4000'), ('ELEM', 'Element')))
    ship_date=forms.DateField(label='Shipping date',widget = forms.SelectDateWidget, input_formats=['%Y-%m-%d'], initial= initial)

class FeaturesSelection(forms.Form):
    features_selection=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=features, label='Select all the features that apply\n')

class StopReason(forms.Form):
    reason_for_stop=forms.CharField(required=True,widget=forms.Textarea)

class ResumeSolution(forms.Form):
    solution = forms.CharField(required=True, widget=forms.Textarea)