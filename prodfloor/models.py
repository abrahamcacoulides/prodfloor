from django.db import models
from django.utils import timezone

class Info(models.Model):
    Tech_name = models.CharField(max_length=50)
    job_num = models.CharField(max_length=10)
    ship_date = models.DateTimeField('Shipping Date')
    status = models.CharField(max_length=50, choices=[('Beginning', 'Beginning'), ('Program', 'Program'), ('Logic', 'Logic'), ('Ending', 'Ending'), ('Complete', 'Complete'),('Stopped', 'Stopped')])
    prev_stage = models.CharField(max_length=50, choices=[('Beginning', 'Beginning'), ('Program', 'Program'), ('Logic', 'Logic'), ('Ending', 'Ending'), ('Complete', 'Complete')])
    current_index = models.IntegerField()
    job_type = models.CharField(max_length=50, choices=[('2000', 'M2000'), ('4000', 'M4000'), ('ELEM', 'Element')])
    stage_len = models.IntegerField()

    def __str__(self):
        return self.job_num

    class Meta:
        verbose_name_plural = 'My Jobs'


class Features(models.Model):
    info=models.ForeignKey(Info)
    features = models.CharField(max_length=200, choices=[('COP','Car Operating Panel'),('HAPS','HAPS battery'),('SHC','Serial Hall Calls')])

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
    reason = models.CharField(max_length=200)
    solution = models.CharField(max_length=200)
    stop_start_time = models.DateTimeField('"Stop" start date')
    stop_end_time = models.DateTimeField('"Stop" finish date')

    class Meta:
        verbose_name_plural = 'Stops per Job'