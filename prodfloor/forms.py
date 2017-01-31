from django import forms
from django.utils import timezone
from django.contrib.auth.models import User

features=(('COP','Car Operating Panel'),('SHC','Serial Hall Calls'),('HAPS','HAPS Battery'),('DCC','Door Control in Cartop'),('CPI','CPI Board Included'),('OVL','Overlay'),('GROUP','Group'),('mView','mView'),('iMon','iMonitor'))
stations = (('1', 'S1'), ('2', 'S2'), ('3', 'S3'),('4', 'S4'),('5', 'S5'),('6', 'S6'),('7', 'S7'),('8', 'S8'),('9', 'S9'),('10', 'S10'),('11', 'S11'),('12', 'S12'),('13', 'ELEM1'),('14', 'ELEM2'))
def getTechs():
    all_techs = User.objects.all()
    techs_list_notup = []
    for tech in all_techs:
        techs_list_notup.append((tech.first_name + ' ' + tech.last_name,tech.first_name + ' ' + tech.last_name))
        global techs_tuple
    techs_tuple=tuple(techs_list_notup)
    return(techs_tuple)

class Maininfo(forms.Form):
    initial = timezone.datetime.today
    job_num = forms.CharField(max_length=10, label='Job #')
    po = forms.CharField(max_length=7, label='Prod #')
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
    reason_for_stop = forms.ChoiceField(required=True,label='Select the reason that fits',choices=(('Reason 1', 'Reason 1'), ('Reason 2', 'Reason 2'), ('Reason 3', 'Reason 3'), ('Reason 4', 'Reason 4'), ('Reason 5', 'Reason 5'),('Reason 6', 'Reason 6')))
    reason_description = forms.CharField(required=True,widget=forms.Textarea)


class ResumeSolution(forms.Form):
    solution = forms.CharField(required=True, widget=forms.Textarea)

class ReassignJob(forms.Form):
    getTechs()
    new_tech = forms.ChoiceField(label='Would be assigned to:', choices=techs_tuple)
    station = forms.ChoiceField(label='Station', choices=stations)
    reason_description = forms.CharField(required=True, widget=forms.Textarea)
