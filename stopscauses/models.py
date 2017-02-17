from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Tier1(models.Model):
    tier_one_cause = models.CharField(max_length=200)

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