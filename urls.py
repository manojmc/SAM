from django.conf.urls.defaults import patterns, url, include
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^sam/$', 'message.views.login1'),
    url(r'^sam/logout1/$', 'message.views.logout1'),
    url(r'^sam/add/$', 'login.views.add_process'),
    url(r'^sam/login/$', 'message.views.login_process'),
    url(r'^sam/ch/$', 'message.views.chartfirst'),
    url(r'^sam/char/$', 'message.views.char'),
    url(r'^sam/(?P<user>\w+)/$', 'message.views.doc'),
    url(r'^sam/patient/$', 'message.views.pat'),
    url(r'^sam/(?P<user>\w+)/logs/$', 'message.views.log'),
    url(r'^sam/(?P<user>\w+)/notes/$', 'message.views.note'),
    url(r'^sam/(?P<user>\w+)/note_process/$', 'message.views.note_process'),
    url(r'^sam/(?P<user>\w+)/datelogs/$', 'message.views.date_log'),
    url(r'^sam/parent/$', 'message.views.par'),
    url(r'^charts/bar/$', 'message.views.barchart'),
    url(r'^sam/(?P<user>\w+)/message/$', 'message.views.msg'),
    url(r'^sam/(?P<user>\w+)/compose/$', 'message.views.msgcompose'),
    url(r'^sam/(?P<user>\w+)/msg/$', 'message.views.process_msg'),
    url(r'^admin/', include(admin.site.urls)),
)
