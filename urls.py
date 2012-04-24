from django.conf.urls.defaults import patterns, url, include
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'message.views.login1'),
    url(r'^sam/logout1/$', 'message.views.logout1'),
    url(r'^sam/(?P<user>\w+)/email/$', 'message.views.send_email1'),
    url(r'^sam/(?P<user>\w+)/upload/$', 'message.views.upload_data'),
    url(r'^sam/login/$', 'message.views.login_process'),
    url(r'^sam/(?P<user>\w+)/ch/$', 'message.views.chartfirst'),
    url(r'^sam/(?P<user>\w+)/char/$', 'message.views.char'),
   # url(r'^sam/(?P<user>\w+)/$', 'message.views.doc'),
    url(r'^sam/(?P<user>\w+)/patient/$', 'message.views.pat'),
    url(r'^sam/(?P<user>\w+)/report/$', 'message.views.gen_report'),
	url(r'^sam/signup/$', 'message.views.signup'),
    url(r'^sam/(?P<user>\w+)/logs/$', 'message.views.log'),
    url(r'^sam/(?P<user>\w+)/notes/$', 'message.views.note'),
    url(r'^sam/(?P<user>\w+)/note_process/$', 'message.views.note_process'),
    url(r'^sam/(?P<user>\w+)/datelogs/$', 'message.views.date_log'),
    url(r'^sam/(?P<user>\w+)/parent/$', 'message.views.par'),
    url(r'^sam/parent/$', 'message.views.par'),
    url(r'^charts/bar/$', 'message.views.barchart'),
    url(r'^sam/(?P<user>\w+)/message/$', 'message.views.msg'),
    url(r'^sam/(?P<user>\w+)/compose/$', 'message.views.msgcompose'),
    url(r'^sam/(?P<user>\w+)/msg/$', 'message.views.process_msg'),
    url(r'^admin/', include(admin.site.urls)),
)
