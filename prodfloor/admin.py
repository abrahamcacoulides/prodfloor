from django.contrib import admin
from .models import Info, Times, Features, Stops
from django.db.models.signals import pre_save,post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

class FeaturesInline(admin.StackedInline):
    verbose_name_plural = _('Features')
    verbose_name = _('Feature')
    model = Features
    extra = 0

class TimesInline(admin.StackedInline):
    verbose_name_plural = _('Times')
    verbose_name = _('Time')
    model = Times
    extra = 0


class MyJob(Info):
    class Meta:
        proxy = True
        verbose_name_plural = _('All Jobs')

class StopsInfo(Info):
    class Meta:
        proxy = True
        verbose_name_plural = _('All Stops')

class InfoAdmin(admin.ModelAdmin):
    actions = None
    readonly_fields = ('po','job_num')
    fieldsets = [
        (None, {'fields': ['po','job_num','label','station','job_type','ship_date']}),
    ]
    inlines = [FeaturesInline]
    list_display = ('job_num','label','station','po','job_type','ship_date', 'status')
    list_filter = ['status']

    def get_queryset(self, request):
        name=request.user.first_name + ' ' + request.user.last_name
        return self.model.objects.filter(Tech_name=name)


class JobsInLine(admin.ModelAdmin):
    readonly_fields = ('Tech_name','status')
    fieldsets = [
        (None, {'fields': ['Tech_name','po', 'job_num','label','station', 'job_type', 'ship_date', 'status']}),
    ]
    inlines = [FeaturesInline, TimesInline]
    list_display = ('Tech_name','job_num','label','station','po', 'job_type', 'ship_date', 'status')


class StopsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['info','po','reason','extra_cause_1','extra_cause_2','reason_description','solution', 'stop_start_time', 'stop_end_time']}),
    ]
    list_display = ('info','po','reason','extra_cause_1','extra_cause_2','solution', 'stop_start_time', 'stop_end_time')


admin.site.register(MyJob,JobsInLine)
admin.site.register(Stops,StopsAdmin)
admin.site.register(Info,InfoAdmin)



#this function sets the current index to 0 if a feature is added/modified/deleted, it would leave the stage at it was previous to the change as it's being->
# assumed that the change was noticed on time; if required admin can do this change
@receiver(pre_save, sender=Features)
@receiver(post_delete, sender=Features)
def my_handler(sender,instance, **kwargs):
    info_obj = instance.info
    info_obj.current_index = 0
    info_obj.save()
