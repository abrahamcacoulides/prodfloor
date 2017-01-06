from django.contrib import admin
from .models import Info, Times, Features, Stops


class FeaturesInline(admin.StackedInline):
    verbose_name_plural = 'Features'
    model = Features
    extra = 0

class TimesInline(admin.StackedInline):
    verbose_name_plural = 'Times'
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
        (None, {'fields': ['Tech_name','job_num','ship_date']}),
    ]
    inlines = [FeaturesInline,TimesInline]
    list_display = ('job_num','Tech_name','ship_date', 'status')

    def get_queryset(self, request):
        name=request.user.first_name + ' ' + request.user.last_name
        return self.model.objects.filter(Tech_name=name)


class JobsInLine(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['Tech_name', 'job_num', 'ship_date', 'status', 'job_type']}),
    ]
    inlines = [FeaturesInline, TimesInline]
    list_display = ('job_num', 'Tech_name', 'ship_date', 'status', 'job_type')


class StopsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['info','reason','solution', 'stop_start_time', 'stop_end_time']}),
    ]
    list_display = ('info','reason','solution', 'stop_start_time', 'stop_end_time')

    #def get_queryset(self, request):
        #return self.model.objects.filter(reason!=)


admin.site.register(MyJob,JobsInLine)
admin.site.register(Stops,StopsAdmin)
admin.site.register(Info,InfoAdmin)