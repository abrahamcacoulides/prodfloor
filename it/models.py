from django.db import models
from django.utils.translation import ugettext_lazy as _
from django import forms

class IT_model(models.Model):
    #auto_id = models.AutoField(primary_key=True)
    issue = models.CharField(max_length=200)
    cause= models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    solution = models.CharField(max_length=200)
    start_time = models.DateTimeField('Issue Start Date')
    end_time = models.DateTimeField('Issue End Date')

    def __str__(self):
        return self.issue

    class Meta:
        verbose_name = _('Server Stop')
        verbose_name_plural = _('Server Stop')

class ServerCauses(models.Model):
    server_issue_causes = models.CharField(max_length=200)

    def __str__(self):
        return self.server_issue_causes

    class Meta:
        verbose_name = _('Server Issues Cause')
        verbose_name_plural = _('Server Issues Causes')