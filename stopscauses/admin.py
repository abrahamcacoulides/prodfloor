from django.contrib import admin
from .models import Tier1,Tier2,Tier3


class Tier1Causes(admin.ModelAdmin):
    fieldsets =[
        (None,
         {'fields': ['tier_one_cause']}),
    ]
    list_display = ('tier_one_cause',)
    search_fields = ['tier_one_cause']
    list_filter = ['tier_one_cause', ]

class Tier2Causes(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['tier_one','tier_two_cause']}),
    ]
    list_display = ('tier_one','tier_two_cause')
    search_fields = ['tier_two_cause']
    list_filter = ['tier_two_cause', ]

    def get_queryset(self, request):
        return self.model.objects.exclude(tier_two_cause='N/A')

class Tier3Causes(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': ['tier_two', 'tier_three_cause']}),
    ]
    list_display = ('get_info','tier_two', 'tier_three_cause')
    search_fields = ['tier_three_cause']
    list_filter = ['tier_three_cause', ]

    def get_info(self, obj):
        return obj.tier_two.tier_one

    get_info.short_description = 'Tier One'
    get_info.admin_order_field = 'tier_two__tier_one'

    def get_queryset(self, request):
        return self.model.objects.exclude(tier_three_cause='N/A')

admin.site.register(Tier1,Tier1Causes)
admin.site.register(Tier2,Tier2Causes)
admin.site.register(Tier3,Tier3Causes)
