from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from prodfloor.views import JobInfo, Stop, ResumeView,Reassign,SuperUserStop,DirectSuperUserStop,StageChange
from . import views

urlpatterns = [
    url(r'^live/M2000/', views.M2000View, name='m2000live'),
    url(r'^live/ELEM/', views.ELEMView, name='elemlive'),
    url(r'^live/M4000/', views.M4000View, name='m4000live'),
    url(r'^su/multiple_reassign/', views.multiplereassigns, name='multipleReassign'),
    url(r'^su/create_stop/', views.createStop, name='createStop'),
    url(r'^su/direct/stop/(?P<pk>[0-9]{1,10})/(?P<po>[0-9]{7})', DirectSuperUserStop.as_view(DirectSuperUserStop.form_list), name='DSUStop'),
    url(r'^su/changestage/(?P<pk>[0-9]{1,10})/(?P<po>[0-9]{7})', StageChange.as_view(StageChange.form_list), name='SUstagechange'),
    url(r'^su/stop/', SuperUserStop.as_view(SuperUserStop.form_list), name='SUStop'),
    url(r'^live/', views.prodfloor_view, name='prodfloor'),
    url(r'^reports/', views.detail, name='detail'),
    url(r'^stops_reports/', views.stops_reports, name='stopsreports'),
    url(r'^stops_techs/', views.stops_reports_techs, name='stopsreportstechs'),
    url(r'^stopdetails/stop/(?P<pk>[0-9]{1,1000})/', views.stopdetail, name='stopdetails'),
    url(r'^generate_report_xml/$', views.generatexml, name='xml'),
    url(r'^generate_stop_report_xml/$', views.generatestopsxml, name='stopsxml'),
    url(r'^endshift/', views.EndShift, name='endshift'),
    url(r'^resume/get_tier_2/', views.get_tier_2, name='t2'),
    url(r'^resume/get_tier_3/', views.get_tier_3, name='t3'),
    url(r'^job/get_stations/', views.get_stations, name='stations'),
    url(r'^first/', views.first, name='first'),
    url(r'^resume',login_required(ResumeView.as_view(ResumeView.form_list))),
    url(r'^job',login_required(JobInfo.as_view(JobInfo.jobs_list))),
    url(r'^reassignjob/(?P<pk>[0-9]{1,10})/(?P<po>[0-9]{7})', login_required(Reassign.as_view(Reassign.list))),
    url(r'^continue/(?P<pk>[0-9]{1,10})/(?P<po>[0-9]{7})', views.Continue, name='returning'),
    url(r'^(?P<action>\w+)/(?P<current_index>[0-9]{1,2})', views.Middle, name='working_on_it'),
    url(r'^stopped',login_required(Stop.as_view(Stop.form_list))),
    url(r'^start/', views.Start, name='new job'),
]