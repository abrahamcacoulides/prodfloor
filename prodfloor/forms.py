from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.utils import timezone
from django.contrib.auth.models import User
from stopscauses.models import Tier1,Tier2,Tier3
from .models import Info
from django.forms import ModelChoiceField,ModelMultipleChoiceField
from prodfloor.dicts import features,stations_tupple
from django.utils.translation import ugettext_lazy as _
from .dicts import label,job_type_tupple,status_dict_tupple,dict_of_stages

class Maininfo(forms.Form):
    initial = timezone.datetime.today
    job_num = forms.CharField(label=_('Job #'),max_length=10)
    po = forms.CharField(label=_('Prod #'),max_length=7)
    label = forms.ChoiceField(label=_('Job label'), choices=label)
    job_type = forms.ChoiceField(label=_('Job type'), choices=job_type_tupple,widget=forms.Select(attrs = {'class':'job_type','id':'job_type'}))
    station = forms.ChoiceField(label=_('Station'), choices=stations_tupple,widget=forms.Select(attrs = {'class':'stations','id':'stations'}))
    ship_date=forms.DateField(label=_('Shipping date'),widget = forms.SelectDateWidget, initial= initial,localize=True)

    def clean(self):
        cleaned_data = super(Maininfo, self).clean()
        job_num = cleaned_data.get('job_num')
        po = cleaned_data.get('po')
        station = cleaned_data.get('station')
        job_type = cleaned_data.get('job_type')
        previous_jobs = Info.objects.all()

        if job_num and po:
            # Only do something if both fields are valid so far.
            if job_num.isdigit() and len(job_num) == 10:
                pass
            else:
                raise forms.ValidationError({'job_num':_("Please validate the 'Job #' input.")})
            if (po.isdigit()) and len(po) == 7:
                if any(po in obj.po for obj in previous_jobs):
                    raise forms.ValidationError({'po':_("The production order number captured is already assigned to someone else.")})
                else:
                    pass
            else:
                raise forms.ValidationError({'po':_("Please validate the 'Prod #' input.")})
            if job_type == '0':
                raise forms.ValidationError({'job_type':_("Please validate the 'Job type' input.")})
            if station == '0':
                raise forms.ValidationError({'station':_("Please validate the 'Station' input.")})

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

class StopReason(forms.Form):
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

class Tier1ChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.tier_one_cause

class ReassignJob(forms.Form):
    new_tech = UserModelChoiceField(queryset=User.objects.filter(groups__name='Technicians'),label=_('Would be assigned to:'))
    station = forms.ChoiceField(label=_('Station'), choices=stations_tupple)
    reason_description = forms.CharField(required=True, widget=forms.Textarea,label=_('Reason'))

class Records(forms.Form):
    job_num = forms.CharField(label=_('Job #'), max_length=10,required=False,help_text='filter by numbers in the Job#',widget=forms.TextInput(attrs={'style':'width:75px'}))
    po = forms.CharField(label=_('Prod #'), max_length=7,required=False,help_text='filter by numbers in the PO#',widget=forms.TextInput(attrs={'style':'width:55px'}))
    status = forms.MultipleChoiceField(label=_('Status'), choices=status_dict_tupple,widget=forms.SelectMultiple(attrs={'style':'width:90px'}),required=False,help_text='filter by Status')
    job_type = forms.MultipleChoiceField(label=_('Job type'), choices=job_type_tupple,widget=forms.SelectMultiple(attrs={'style':'width:80px'}),required=False,help_text='filter by Type')
    station = forms.MultipleChoiceField(label=_('Station'), choices=stations_tupple,widget=forms.SelectMultiple(attrs={'style':'width:80px'}),required=False,help_text='filter by Station')
    after = forms.DateField(label=_('Min Start Date'),help_text='filter by the start date',widget=AdminDateWidget,required=False)
    before = forms.DateField(label=_('Max Start Date'),help_text='filter by the start date',widget=AdminDateWidget,required=False)
    completed_after = forms.DateField(label=_('Min Completion Date'),help_text='filter by the end date', widget=AdminDateWidget, required=False)
    completed_before = forms.DateField(label=_('Max Completion Date'),help_text='filter by the end date', widget=AdminDateWidget, required=False)
    tech = UserModelChoiceField(queryset=User.objects.filter(groups__name='Technicians'),help_text=_('Was assigned to:'), required=False)

class StopRecord(forms.Form):
    job_num = forms.CharField(label=_('Job #'), max_length=10, required=False,help_text='filter by numbers in the Job#',widget=forms.TextInput(attrs={'style': 'width:75px'}))
    po = forms.CharField(label=_('Prod #'), max_length=7, required=False, help_text='filter by numbers in the PO#',widget=forms.TextInput(attrs={'style': 'width:55px'}))
    reason = Tier1ChoiceField(label=_('Reason'),queryset=Tier1.objects.all(),widget=forms.SelectMultiple(attrs={'style': 'width:180px'}), required=False,help_text='filter by Stop Reason',to_field_name="tier_one_cause")
    job_type = forms.MultipleChoiceField(label=_('Job type'), choices=job_type_tupple,widget=forms.SelectMultiple(attrs={'style': 'width:80px'}), required=False,help_text='filter by Type')
    station = forms.MultipleChoiceField(label=_('Station'), choices=stations_tupple,widget=forms.SelectMultiple(attrs={'style': 'width:80px'}), required=False,help_text='filter by Station')
    after = forms.DateField(label=_('Min Start Date'), help_text='filter by the start date', widget=AdminDateWidget,required=False)
    before = forms.DateField(label=_('Max Start Date'), help_text='filter by the start date', widget=AdminDateWidget,required=False)
    completed_after = forms.DateField(label=_('Min Completion Date'), help_text='filter by the end date',widget=AdminDateWidget, required=False)
    completed_before = forms.DateField(label=_('Max Completion Date'), help_text='filter by the end date',widget=AdminDateWidget, required=False)

class SUStop(forms.Form):
    job_num = forms.CharField(label=_('Job #'), max_length=10, help_text='filter by numbers in the Job#',)
    po = forms.CharField(label=_('Prod #'), max_length=7, help_text='filter by numbers in the PO#')

    def clean(self):
        cleaned_data = super(SUStop, self).clean()
        job_num = cleaned_data.get('job_num')
        po = cleaned_data.get('po')
        previous_jobs = Info.objects.all()

        if job_num and po:
            # Only do something if both fields are valid so far.
            if job_num.isdigit() and len(job_num) == 10:
                pass
            else:
                raise forms.ValidationError({'job_num':_("Please validate the 'Job #' input.")})
            if (po.isdigit()) and len(po) == 7:
                if any(po in obj.po for obj in previous_jobs):
                    try:
                        job_with_po = Info.objects.exclude(status='Complete').exclude(status="Reassigned").exclude('Stopped').get(po=po)
                    except:
                        raise forms.ValidationError( {'po': _("This job is not active. Please confirm the status of this job.")})
                    if job_num != job_with_po.job_num:
                        raise forms.ValidationError({'job_num': _("The job number doesn't match the one for that po in the system.")})
                else:
                    raise forms.ValidationError({'po': _("The production order number captured is not in the system.")})
            else:
                raise forms.ValidationError({'po':_("Please validate the 'Prod #' input.")})

class MultipleReassign(forms.Form):
    tobeupdated = forms.BooleanField(required=False,)
    job_num = forms.CharField(required=False,label=_('Job #'), max_length=10,widget=forms.TextInput(attrs = {'readonly':True}))
    po = forms.CharField(required=False,label=_('Prod #'), max_length=7,widget=forms.TextInput(attrs = {'readonly':True}))
    new_tech = UserModelChoiceField(required=False,queryset=User.objects.filter(groups__name='Technicians'),label=_('Would be assigned to'))
    station = forms.ChoiceField(required=False,label=_('Station'), choices=stations_tupple)
    reason_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'style': 'height:18px;width:200px'}), label=_('Reason'))

    def clean(self):
        cleaned_data = super(MultipleReassign, self).clean()
        update = cleaned_data.get('tobeupdated')
        po = cleaned_data.get('po')
        new_tech = cleaned_data.get('new_tech')
        station = cleaned_data.get('station')
        reason = cleaned_data.get('reason_description')
        job = Info.objects.exclude(status="Complete").exclude(status="Reassigned").get(po=po)
        if update:
            if not new_tech:
                raise forms.ValidationError(
                    {'new_tech': _("This field is required.")})
            if not station:
                raise forms.ValidationError(
                    {'station': _("This field is required.")})
            if not reason:
                raise forms.ValidationError(
                    {'reason_description': _("This field is required.")})
            if job.Tech_name == new_tech.first_name + ' ' + new_tech.last_name and job.station == station:
                raise forms.ValidationError(
                    {'new_tech': _("No change."),'station': _("No change.")})
        else:
            if job.Tech_name != new_tech.first_name + ' ' + new_tech.last_name or job.station != station:
                raise forms.ValidationError(
                    {'tobeupdated': _("Select the checkbox.")})

class ChangeStage(forms.Form):
    current_stage = forms.CharField(label=_('Current Stage'), widget=forms.TextInput(attrs={'readonly':True}))
    new_stage = forms.ChoiceField(label=_('New Stage'), choices=status_dict_tupple)
    def clean(self):
        cleaned_data = super(ChangeStage, self).clean()
        current = cleaned_data.get('current_stage')
        new = cleaned_data.get('new_stage')
        if current == 'Complete':
            raise forms.ValidationError(
                {'current_stage': _("The job is marked as complete. If job needs to be worked on please use the Rework function.")})
        elif current == 'Reassigned':
            raise forms.ValidationError(
                {'current_stage': _("The job is marked as reassigned therefore it's no longer available to change state.")})
        elif current == 'Stopped':
            raise forms.ValidationError(
                {'current_stage': _("The job is marked as Stopped; The job must be active in order to have a change of stage.")})
        elif new == 'Reassigned':
            raise forms.ValidationError(
                {'new_stage': _("If you'd like to reassign this job please use the specific function for this.")})
        elif new == 'Rework':
            raise forms.ValidationError(
                {'new_stage': _(
                    "If you'd like to log a rework for this job please use the specific function for this.")})
        elif list(dict_of_stages.keys())[list(dict_of_stages.values()).index(current)]<list(dict_of_stages.keys())[list(dict_of_stages.values()).index(new)]:
            raise forms.ValidationError(
                {'new_stage': _("This function is not supposed to be used to skip stages.")})
        else:
            if current == new:
                raise forms.ValidationError(
                    {'new_stage': _("The current and new stage are the same.")})
