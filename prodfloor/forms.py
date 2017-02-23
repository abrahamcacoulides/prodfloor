from django import forms
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from stopscauses.models import Tier1,Tier2,Tier3
from .models import Info
from django.forms import ModelChoiceField
from prodfloor.dicts import features,stations
from datetime import date
from django.utils.translation import ugettext_lazy as _
from .dicts import label,job_type

class Maininfo(forms.Form):
    initial = timezone.datetime.today
    job_num = forms.CharField(label=_('Job #'),max_length=10)
    po = forms.CharField(label=_('Prod #'),max_length=7)
    label = forms.ChoiceField(label=_('Job label'), choices=label)
    job_type = forms.ChoiceField(label=_('Job type'), choices=job_type)
    station = forms.ChoiceField(label=_('Station'), choices=stations)
    ship_date=forms.DateField(label=_('Shipping date'),widget = forms.SelectDateWidget, initial= initial,localize=True)

    def clean(self):
        cleaned_data = super(Maininfo, self).clean()
        job_num = cleaned_data.get('job_num')
        po = cleaned_data.get('po')
        previous_jobs = Info.objects.all()

        if job_num and po:
            # Only do something if both fields are valid so far.
            if job_num.isdigit() and len(job_num) == 10:
                pass
            else:
                raise forms.ValidationError(
                    _("Please validate the 'Job #' input.")
                )
            if (po.isdigit()) and len(po) == 7:
                if any(po in obj.po for obj in previous_jobs):
                    raise forms.ValidationError(
                        _("The production order number captured is already assigned to someone else.")
                    )
                else:
                    pass
            else:
                raise forms.ValidationError(
                    _("Please validate the 'Prod #' input.")
                )



class FeaturesSelection(forms.Form):
    features_selection=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=features, label=_('Select all the features that apply\n'))

    def clean(self):
        cleaned_data = super(FeaturesSelection, self).clean()
        features = cleaned_data.get('features_selection')
        if features:
            if any(obj == 'None' for obj in features) and any(obj != 'None' for obj in features):
                raise forms.ValidationError(
                    _("You selected 'None' but also another feature, please confirm your selections.")
                )


class StopReason(forms.Form):#TODO valid reasons for stops
    reason_for_stop = forms.ModelChoiceField(required=True,label=_('Select the reason that fits'),queryset=Tier1.objects.all())
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
    tier1=forms.CharField(required=True,label=_('Cause'), widget=forms.TextInput(attrs = {'class':'tier1','id':'tier1','readonly':True}))
    tier2=forms.ChoiceField(choices=choices_tier_2_tupple,label=_('First reason'),widget=forms.Select(attrs = {'class':'tier2','id':'tier2'}))
    tier3=forms.ChoiceField(choices=choices_tier_3_tupple,label=_('Second reason'),widget=forms.Select(attrs = {'class':'tier3','id':'tier3'}))
    solution = forms.CharField(required=True, widget=forms.Textarea)

class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class ReassignJob(forms.Form):
    new_tech = UserModelChoiceField(queryset=User.objects.filter(groups__name='Technicians'),label=_('Would be assigned to:'))
    station = forms.ChoiceField(label=_('Station'), choices=stations)
    reason_description = forms.CharField(required=True, widget=forms.Textarea,label=_('Reason'))
