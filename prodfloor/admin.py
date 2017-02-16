from django.contrib import admin
from .models import Info, Times, Features, Stops,Tier1,Tier2,Tier3


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
        (None, {'fields': ['po','job_num','label','station','job_type','ship_date']}),
    ]
    inlines = [FeaturesInline,TimesInline]
    list_display = ('job_num','label','station','po','job_type','ship_date', 'status')
    list_filter = ['status']

    def get_queryset(self, request):
        name=request.user.first_name + ' ' + request.user.last_name
        return self.model.objects.filter(Tech_name=name)


class JobsInLine(admin.ModelAdmin):
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

class Tier1Causes(admin.ModelAdmin):
    fieldsets =[
        (None,
         {'fields': ['tier_one_cause']}),
    ]
    list_display = ('tier_one_cause',)

class Tier2Causes(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['tier_one','tier_two_cause']}),
    ]
    list_display = ('tier_one','tier_two_cause')

    def get_queryset(self, request):
        return self.model.objects.exclude(tier_two_cause='N/A')

class Tier3Causes(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['tier_two', 'tier_three_cause']}),
    ]
    list_display = ('get_info','tier_two', 'tier_three_cause')

    def get_info(self, obj):
        return obj.tier_two.tier_one

    get_info.short_description = 'Tier One'
    get_info.admin_order_field = 'tier_two__tier_one'

    def get_queryset(self, request):
        return self.model.objects.exclude(tier_three_cause='N/A')


admin.site.register(MyJob,JobsInLine)
admin.site.register(Stops,StopsAdmin)
admin.site.register(Info,InfoAdmin)
admin.site.register(Tier1,Tier1Causes)
admin.site.register(Tier2,Tier2Causes)
admin.site.register(Tier3,Tier3Causes)
