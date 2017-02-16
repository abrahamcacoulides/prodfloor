from django.db import models
from django.utils.translation import ugettext_lazy as _
from prodfloor.dicts import stop_reasons, stations_dict,status_dict,type_of_jobs,features_list

class Info(models.Model):
    Tech_name = models.CharField(max_length=50)
    job_num = models.CharField(max_length=10)
    po = models.CharField(max_length=7)
    ship_date = models.DateTimeField('Shipping Date')
    status = models.CharField(max_length=50, choices=status_dict)
    prev_stage = models.CharField(max_length=50, choices=[('Beginning', 'Beginning'),
                                                          ('Program', 'Program'),
                                                          ('Logic', 'Logic'),
                                                          ('Ending', 'Ending'),
                                                          ('Complete', 'Complete')])
    station = models.CharField(max_length=2,choices=stations_dict)
    label = models.CharField(max_length=1)
    current_index = models.IntegerField()
    job_type = models.CharField(max_length=50, choices=type_of_jobs)
    stage_len = models.IntegerField()

    def __str__(self):
        return self.job_num

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('My Jobs')


class Features(models.Model):
    info=models.ForeignKey(Info)
    features = models.CharField(max_length=200, choices=features_list)

class Times(models.Model):
    info = models.ForeignKey(Info)
    po = models.CharField(max_length=7)
    start_time_1 = models.DateTimeField('"Inicio de Test" start date')
    end_time_1 = models.DateTimeField('"Inicio de Test" finish date')
    start_time_2 = models.DateTimeField('"Programacion" start date')
    end_time_2 = models.DateTimeField('"Programacion" finish date')
    start_time_3 = models.DateTimeField('"Pruebas logicas" start date')
    end_time_3 = models.DateTimeField('"Pruebas logicas" finish date')
    start_time_4 = models.DateTimeField('"Fin de Test" start date')
    end_time_4 = models.DateTimeField('"Fin de Test" finish date')

class Stops(models.Model):
    info = models.ForeignKey(Info)
    po = models.CharField(max_length=7)
    reason = models.CharField(max_length=200)
    extra_cause_1 = models.CharField(max_length=200)
    extra_cause_2 = models.CharField(max_length=200)
    reason_description = models.CharField(max_length=200)
    solution = models.CharField(max_length=200)
    stop_start_time = models.DateTimeField('"Stop" start date')
    stop_end_time = models.DateTimeField('"Stop" finish date')

    class Meta:
        verbose_name_plural = _('Stops per Job')

class Tier1(models.Model):
    tier_one_cause = models.CharField(max_length=200,choices=stop_reasons)

    def __str__(self):
        return self.tier_one_cause

    class Meta:
        verbose_name = _('First Level Cause')
        verbose_name_plural = _('First Level Causes')

class Tier2(models.Model):
    tier_two_cause = models.CharField(max_length=200)
    tier_one = models.ForeignKey(Tier1)

    def __str__(self):
        return self.tier_two_cause

    class Meta:
        verbose_name = _('Second Level Cause')
        verbose_name_plural = _('Second Level Causes')

class Tier3(models.Model):
    tier_three_cause = models.CharField(max_length=200)
    tier_two = models.ForeignKey(Tier2)

    def __str__(self):
        return self.tier_three_cause

    class Meta:
        verbose_name = _('Third Level Cause')
        verbose_name_plural = _('Third Level Causes')
