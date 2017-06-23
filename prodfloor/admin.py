from django.contrib import admin
from django.contrib.admin.options import get_content_type_for_model
from django.core.exceptions import PermissionDenied
from django.template.defaultfilters import capfirst
from django.template.response import TemplateResponse
from django.utils.encoding import force_text

from .models import Info, Times, Features, Stops
from django.db.models.signals import pre_save,post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.utils import (
    NestedObjects, construct_change_message, flatten_fieldsets,
    get_deleted_objects, lookup_needs_distinct, model_format_dict, quote,
    unquote,
)

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
    search_fields = ['job_num','ship_date']

    def history_view(self, request, object_id, extra_context=None):
        "The 'history' admin view for this model."
        from django.contrib.admin.models import LogEntry
        # First check if the user can see this history.
        model = self.model
        obj = self.get_object(request, unquote(object_id))
        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, model._meta, object_id)

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        # Then get the history for this object.
        opts = model._meta
        app_label = opts.app_label
        #if request.user.is_superuser:
        #    action_list = LogEntry.objects.filter(
        #        object_id=unquote(object_id)
        #    ).select_related().order_by('action_time')
        #else:
        #    action_list = LogEntry.objects.filter(
        #        object_id=unquote(object_id),
        #        content_type=get_content_type_for_model(model)
        #    ).select_related().order_by('action_time')
        action_list = LogEntry.objects.filter(object_id=unquote(object_id)).select_related().order_by('action_time')

        context = dict(
            self.admin_site.each_context(request),
            title=_('Change history: %s') % force_text(obj),
            action_list=action_list,
            module_name=capfirst(force_text(opts.verbose_name_plural)),
            object=obj,
            opts=opts,
            preserved_filters=self.get_preserved_filters(request),
        )
        context.update(extra_context or {})

        request.current_app = self.admin_site.name

        return TemplateResponse(request, self.object_history_template or [
            "admin/%s/%s/object_history.html" % (app_label, opts.model_name),
            "admin/%s/object_history.html" % app_label,
            "admin/object_history.html"
        ], context)


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
    stops = Stops.objects.filter(info_id=info_obj.pk).filter(reason='Job reassignment')
    if any(stop.solution == 'Not available yet' for stop in stops):
        Go = False
    else:
        Go = True
    if Go:
        info_obj.current_index = 0
        info_obj.save()


