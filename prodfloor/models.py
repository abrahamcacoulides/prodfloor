from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class Info(models.Model):
    Tech_name = models.CharField(max_length=50)
    job_num = models.CharField(max_length=10)
    po = models.CharField(max_length=7)
    ship_date = models.DateTimeField('Shipping Date')
    status = models.CharField(max_length=50, choices=[('Beginning', 'Beginning'),
                                                      ('Program', 'Program'),
                                                      ('Logic', 'Logic'),
                                                      ('Ending', 'Ending'),
                                                      ('Complete', 'Complete'),
                                                      ('Stopped', 'Stopped')])
    prev_stage = models.CharField(max_length=50, choices=[('Beginning', 'Beginning'),
                                                          ('Program', 'Program'),
                                                          ('Logic', 'Logic'),
                                                          ('Ending', 'Ending'),
                                                          ('Complete', 'Complete')])
    label = models.CharField(max_length=1)
    current_index = models.IntegerField()
    job_type = models.CharField(max_length=50, choices=[('2000', 'M2000'), ('4000', 'M4000'), ('ELEM', 'Element')])
    stage_len = models.IntegerField()

    def __str__(self):
        return self.job_num

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('My Jobs')


class Features(models.Model):
    info=models.ForeignKey(Info)
    features = models.CharField(max_length=200, choices=[('COP','Car Operating Panel'),
                                                         ('SHC','Serial Hall Calls'),
                                                         ('HAPS','HAPS battery'),
                                                         ('OVL','Overlay'),
                                                         ('GROUP','Group'),
                                                         ('mView','mView'),
                                                         ('iMon','iMonitor')])

class Times(models.Model):
    info = models.ForeignKey(Info)
    start_time_1 = models.DateTimeField('"Inicio de Test" start date')
    end_time_1 = models.DateTimeField('"Inicio de Test" finish date')
    start_time_2 = models.DateTimeField('"Programacion" start date')
    end_time_2 = models.DateTimeField('"Programacion" finish date')
    start_time_3 = models.DateTimeField('"Pruebas logicas" start date')
    end_time_3 = models.DateTimeField('"Pruebas logicas" finish date')
    start_time_4 = models.DateTimeField('"Fin de Test" start date')
    end_time_4 = models.DateTimeField('"Fin de Test" finish date')

    def timeelapsed(self):
        now = timezone.now()
        return now - self.start_time

class Stops(models.Model):
    info = models.ForeignKey(Info)
    reason = models.CharField(max_length=200,choices=[('Job reassignment', 'Job reassignment'),
                                                      ('Shift ended','Shift ended'),
                                                      ('Reason 1', 'Reason 1'),
                                                      ('Reason 2', 'Reason 2'),
                                                      ('Reason 3', 'Reason 3'),
                                                      ('Reason 4', 'Reason 4'),
                                                      ('Reason 5', 'Reason 5'),
                                                      ('Reason 6', 'Reason 6')])
    reason_description = models.CharField(max_length=200)
    solution = models.CharField(max_length=200)
    stop_start_time = models.DateTimeField('"Stop" start date')
    stop_end_time = models.DateTimeField('"Stop" finish date')

    class Meta:
        verbose_name_plural = _('Stops per Job')