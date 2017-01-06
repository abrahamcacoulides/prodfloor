from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from prodfloor.views import JobInfo, Stop, ResumeView

from . import views

urlpatterns = [
    url(r'^live/', views.prodfloor_view, name='prodfloor'),
    url(r'^(?P<info_job_num>[0-9]{10})/$', views.detail, name='detail'),
    url(r'^stop',login_required(Stop.as_view(Stop.form_list))),
    url(r'^resume',login_required(ResumeView.as_view(ResumeView.form_list))),
    url(r'^job',login_required(JobInfo.as_view(JobInfo.jobs_list))),
    url(r'^continue/(?P<jobnum>[0-9]{10})', views.Continue, name='returning'),
    url(r'^end/(?P<action>\w+)', views.Middle, name='working_on_it'),
    url(r'^end/', views.Start, name='new job'),
]