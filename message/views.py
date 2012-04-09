	# Create your views here.
from message.models import user_table, message_table, log_table, notes_table
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import 	MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from login.models import UserProfile
import datetime
from GChartWrapper import *
from django.utils import simplejson

def login1(request):
	#user_profile = request.user.get_profile()
	#url = user_profile.url
	return render_to_response('message/login.html')
	
@csrf_exempt
def login_process(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:	
			login(request, user)
			t = UserProfile.objects.get(user=user.id)
			if t.type == 1:
				return render_to_response('message/pat.html', {'user': user
				}, context_instance=RequestContext(request))
	else:
		return HttpResponse("authentication failed")
		

@csrf_exempt				
def logout1(request):
	logout(request)
	return render_to_response('message/login.html')
				
def pat(request):
	return HttpResponse("this is the patient page")
	
def par(request):
	return HttpResponse("this is the parent page")

@csrf_exempt
def note(request, user):

	u=get_object_or_404(User, username=user)
	date = datetime.date.today()
	start_week = date - datetime.timedelta(date.weekday())
	end_week = start_week + datetime.timedelta(6)
	l_note = notes_table.objects.filter(uid=u.id, start_week__range=[start_week, end_week]).order_by('start_week')
	return render_to_response("message/note.html", {'user': user, 'note_list': l_note, 
	'start_week': start_week, 
	'end_week': end_week
	}, context_instance=RequestContext(request))

@csrf_exempt
def note_process(request, user):

	u=get_object_or_404(User, username=user)
	flag = request.POST['flag']
	if flag == 'set':
		date = datetime.datetime.strptime(request.POST['u_date'], '%Y-%m-%d').date()
		start_week = date - datetime.timedelta(date.weekday())
		end_week = start_week + datetime.timedelta(6)
	
		l_note = notes_table.objects.filter(uid=u.id, start_week__range=[start_week, end_week]).order_by('start_week')
		return render_to_response("message/note.html", {'user': user, 'note_list': l_note, 
		'start_week': start_week, 
		'end_week': end_week
		}, context_instance=RequestContext(request))

	
	else:
		date = datetime.datetime.strptime(request.POST['u_date'], '%Y-%m-%d').date()
		#date = request.POST['u_date']
		note = request.POST['u_note']

		start_week = date - datetime.timedelta(date.weekday())
		end_week = start_week + datetime.timedelta(6)

		u.notes_table_set.create(uid=u.id, start_week = start_week, end_week = end_week, note = note)

		l_note = notes_table.objects.filter(uid=u.id, start_week__range=[start_week, end_week]).order_by('start_week')
		return render_to_response("message/note.html", {'user': user, 'note_list': l_note, 
		'start_week': start_week, 
		'end_week': end_week
		}, context_instance=RequestContext(request))
	
def msgcompose(request, user):
	return render_to_response("message/msgcompose.html", {
		'user': user,
	}, context_instance=RequestContext(request))

@login_required(login_url='/sam/')
def log(request, user):
	
	u=get_object_or_404(User, username=user)
	
	date = datetime.date.today()
	start_week = date - datetime.timedelta(date.weekday())
	end_week = start_week + datetime.timedelta(7)
	
	l_list = log_table.objects.filter(uid=u.id, timestamp__range=[start_week, end_week]).order_by('timestamp')
	
	return render_to_response('message/log.html', {'log_list': l_list, 'user': u})

@csrf_exempt	
def date_log(request, user):
	
	u=get_object_or_404(User, username=user)
	
	
	start_week = request.POST['from_date']
	end_week = request.POST['to_date']
	l_list = log_table.objects.filter(uid=u.id, timestamp__range=[start_week, end_week]).order_by('timestamp')
	
	return render_to_response('message/log.html', {'log_list': l_list, 'user': u})

@csrf_exempt
def chartfirst(request):
	return render_to_response("message/chart.html")
	
@csrf_exempt	
def char(request):
	user_date = request.POST['f_date']
	user = request.POST['user_name']
	u = get_object_or_404 (user_table,username = user)
	
	user_date = datetime.datetime.strptime(request.POST['f_date'], '%Y-%m-%d').date()
	start_week = user_date - datetime.timedelta(user_date.weekday())
	
	#for x in range(0,7):
	end_week = start_week + datetime.timedelta(1)
	data1 = 'Monday'
	
	data4 = log_table.objects.filter(uid=u.id, timestamp__range=[start_week, end_week], med_id = 1).count()
	data5 = log_table.objects.filter(uid=u.id, timestamp__range=[start_week, end_week], med_id = 2).count()
	data6 = log_table.objects.filter(uid=u.id, timestamp__range=[start_week, end_week], med_id = 3).count()
	print data4
	print data5
	print data6
	print start_week
	print end_week
	count_medicine = data4 + data5 + data6

	sym1 = log_table.objects.filter(uid=u.id, timestamp__range=[start_week, end_week], med_id = 4).count()
	sym2 = log_table.objects.filter(uid=u.id, timestamp__range=[start_week, end_week], med_id = 5).count()
	sym3 = log_table.objects.filter(uid=u.id, timestamp__range=[start_week, end_week], med_id = 6).count()
	
	count_symptom = sym1 + sym2 + sym3
	print count_medicine 
	count = ['monday', count_medicine, count_symptom]
	
	return render_to_response('message/chart.html', {'data4': count})
	#return render_to_response('message/chart.html', {'json_list': json_list})
	#return render_to_response('message/chart.html', {'data1': data1, 'data2': data2, 'data3': data3})

@csrf_exempt	
def process_msg(request, user):
	
	try:
		sender = request.POST['from']
		reciever = request.POST['to']
		message = request.POST['message']
		u = get_object_or_404(user_table, username=sender)
				
	except (KeyError, Http404):
		return render_to_response('message/msgcompose.html', {
            'error_message': "Please enter the required information!!",
        }, context_instance=RequestContext(request)) 
        
	else:
		try:
			r = get_object_or_404(user_table, username=reciever)
			
		except (KeyError, Http404):
			return render_to_response('message/msgcompose.html', {
				'user': user,
				'rec_error': "Reciever address incorrect",
			}, context_instance=RequestContext(request))
			
		else:
			u.message_table_set.create(sender=sender, reciever=reciever, message=message)
			return render_to_response("message/sent.html", {
				'user': user, 
				'sent_ack': "Message sent Successfull!!",
			}, context_instance=RequestContext(request))
