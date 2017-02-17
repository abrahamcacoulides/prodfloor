from django import forms
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from stopscauses.models import Tier1,Tier2,Tier3
from django.forms import ModelChoiceField
from prodfloor.dicts import features,stations
from datetime import date

class Maininfo(forms.Form):
    year_value = date.today().year + 2
    value = year_value * 1000000
    value2 = date.today().year * 1000000
    initial = timezone.datetime.today
    job_num = forms.IntegerField(label='Job #',validators=[MaxValueValidator(value),MinValueValidator(value2)])
    po = forms.IntegerField(label='Prod #',validators=[MaxValueValidator(9999999),MinValueValidator(3000000)])
    label = forms.ChoiceField(label='Job label', choices=(('-', '-'),
                                                          ('A', 'A'),
                                                          ('B', 'B'),
                                                          ('C', 'C'),
                                                          ('D', 'D'),
                                                          ('E', 'E'),
                                                          ('F', 'F'),
                                                          ('G', 'G'),
                                                          ('H', 'H')))
    job_type = forms.ChoiceField(label='Job type', choices=(('2000', 'M2000'), ('4000', 'M4000'), ('ELEM', 'Element')))
    station = forms.ChoiceField(label='Station', choices=stations)
    ship_date=forms.DateField(label='Shipping date',widget = forms.SelectDateWidget, input_formats=['%Y-%m-%d'], initial= initial)


class FeaturesSelection(forms.Form):
    features_selection=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=features, label='Select all the features that apply\n')


class StopReason(forms.Form):#TODO valid reasons for stops
    reason_for_stop = forms.ModelChoiceField(required=True,label='Select the reason that fits',queryset=Tier1.objects.all())
    reason_description = forms.CharField(required=True,widget=forms.Textarea)


class ResumeSolution(forms.Form):
    choices_tier_2 = []
    choices_tier_3 = [('------','------')]
    for obj in Tier2.objects.all():
        choices_tier_2.append((obj.tier_two_cause,obj.tier_two_cause))
    choices_tier_2_tupple = tuple(choices_tier_2)
    for obj in Tier3.objects.all():
        choices_tier_3.append((obj.tier_three_cause,obj.tier_three_cause))
    choices_tier_3_tupple = tuple(choices_tier_3)
    tier1=forms.CharField(required=True, widget=forms.TextInput(attrs = {'class':'tier1','id':'tier1','readonly':True}))
    tier2=forms.ChoiceField(choices=choices_tier_2_tupple,widget=forms.Select(attrs = {'class':'tier2','id':'tier2'}))
    tier3=forms.ChoiceField(choices=choices_tier_3_tupple,widget=forms.Select(attrs = {'class':'tier3','id':'tier3'}))
    solution = forms.CharField(required=True, widget=forms.Textarea)

class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class ReassignJob(forms.Form):
    new_tech = UserModelChoiceField(queryset=User.objects.filter(groups__name='Technicians'),label='Would be assigned to:')
    station = forms.ChoiceField(label='Station', choices=stations)
    reason_description = forms.CharField(required=True, widget=forms.Textarea)
