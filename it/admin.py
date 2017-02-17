from django.contrib import admin
from .models import IT_model, ServerCauses

class ITadmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['issue','status','cause','solution', 'start_time','end_time']}),
    ]
    list_display = ('issue','status','cause','solution', 'start_time','end_time')

    def get_queryset(self, request):
        return self.model.objects.exclude(status='Complete')

class Causes(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['server_issue_causes',]}),
    ]
    list_display = ('server_issue_causes',)


admin.site.register(IT_model,ITadmin)
admin.site.register(ServerCauses,Causes)
