from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from prodfloor.views import JobInfo, Stop, ResumeView,Reassign

from . import views

urlpatterns = [
    url(r'^live/M2000/', views.M2000View, name='m2000live'),
    url(r'^live/ELEM/', views.ELEMView, name='elemlive'),
    url(r'^live/M4000/', views.M4000View, name='m4000live'),
    url(r'^live/', views.prodfloor_view, name='prodfloor'),
    url(r'^(?P<info_job_num>[0-9]{10})/$', views.detail, name='detail'),
    url(r'^endshift/', views.EndShift, name='endshift'),
    url(r'^resume/get_tier_2/', views.get_tier_2, name='t2'),
    url(r'^resume/get_tier_3/', views.get_tier_3, name='t3'),
    url(r'^first/', views.first, name='first'),
    url(r'^resume',login_required(ResumeView.as_view(ResumeView.form_list))),
    url(r'^job',login_required(JobInfo.as_view(JobInfo.jobs_list))),
    url(r'^reassignjob/(?P<jobnum>[0-9]{10})/(?P<po>[0-9]{7})', login_required(Reassign.as_view(Reassign.list))),
    url(r'^continue/(?P<jobnum>[0-9]{10})/(?P<po>[0-9]{7})', views.Continue, name='returning'),
    url(r'^(?P<action>\w+)/(?P<current_index>[0-9]{1,2})', views.Middle, name='working_on_it'),
    url(r'^stopped',login_required(Stop.as_view(Stop.form_list))),
    url(r'^start/', views.Start, name='new job'),
]