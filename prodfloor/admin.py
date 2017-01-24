from django.contrib import admin
from .models import Info, Times, Features, Stops


class FeaturesInline(admin.StackedInline):
    verbose_name_plural = 'Features'
    verbose_name = 'Feature'
    model = Features
    extra = 0

class TimesInline(admin.StackedInline):
    verbose_name_plural = 'Times'
    verbose_name = 'Time'
    model = Times
    extra = 0


class MyJob(Info):
    class Meta:
        proxy = True
        verbose_name_plural = 'All Jobs'

class StopsInfo(Info):
    class Meta:
        proxy = True
        verbose_name_plural = 'All Stops'

class InfoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['Tech_name','po','job_num','label','job_type','ship_date']}),
    ]
    inlines = [FeaturesInline,TimesInline]
    list_display = ('job_num','label','Tech_name','po','job_type','ship_date', 'status')

    def get_queryset(self, request):
        name=request.user.first_name + ' ' + request.user.last_name
        return self.model.objects.filter(Tech_name=name)


class JobsInLine(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['Tech_name','po', 'job_num','label', 'job_type', 'ship_date', 'status']}),
    ]
    inlines = [FeaturesInline, TimesInline]
    list_display = ('Tech_name','job_num','label','po', 'job_type', 'ship_date', 'status')


class StopsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['info','reason','reason_description','solution', 'stop_start_time', 'stop_end_time']}),
    ]
    list_display = ('info','reason','solution', 'stop_start_time', 'stop_end_time')


admin.site.register(MyJob,JobsInLine)
admin.site.register(Stops,StopsAdmin)
admin.site.register(Info,InfoAdmin)