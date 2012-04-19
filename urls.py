from django.conf.urls.defaults import patterns, url, include
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
<<<<<<< HEAD
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
=======
    url(r'^sam/$', 'message.views.login1'),
    url(r'^sam/logout1/$', 'message.views.logout1'),
    url(r'^sam/add/$', 'login.views.add_process'),
    url(r'^sam/login/$', 'message.views.login_process'),
    url(r'^sam/ch/$', 'message.views.chartfirst'),
    url(r'^sam/char/$', 'message.views.char'),
    url(r'^sam/(?P<user>\w+)/$', 'message.views.doc'),
    url(r'^sam/patient/$', 'message.views.pat'),
>>>>>>> c6f766ec206fa295a6dfca213cfb53e641f0a5f9
    url(r'^sam/(?P<user>\w+)/logs/$', 'message.views.log'),
    url(r'^sam/(?P<user>\w+)/notes/$', 'message.views.note'),
    url(r'^sam/(?P<user>\w+)/note_process/$', 'message.views.note_process'),
    url(r'^sam/(?P<user>\w+)/datelogs/$', 'message.views.date_log'),
<<<<<<< HEAD
    url(r'^sam/(?P<user>\w+)/parent/$', 'message.views.par'),
=======
    url(r'^sam/parent/$', 'message.views.par'),
>>>>>>> c6f766ec206fa295a6dfca213cfb53e641f0a5f9
    url(r'^charts/bar/$', 'message.views.barchart'),
    url(r'^sam/(?P<user>\w+)/message/$', 'message.views.msg'),
    url(r'^sam/(?P<user>\w+)/compose/$', 'message.views.msgcompose'),
    url(r'^sam/(?P<user>\w+)/msg/$', 'message.views.process_msg'),
    url(r'^admin/', include(admin.site.urls)),
)
