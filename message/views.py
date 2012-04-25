	# Create your views here.
from message.models import *
#from message.models import user_table, message_table, log_table, log_form, notes_table, relation_table, LogTable
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from login.models import UserProfile
import datetime
from random import randint
#from GChartWrapper import *
from django.utils import simplejson
from django.core.mail import send_mail,EmailMultiAlternatives
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.template.loader import get_template
from django.template import Context

import sys,os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from message.models import LogTable
import csv


@csrf_exempt
def upload_data(request, user):
	
	u = User.objects.get(username=user)
	t = UserProfile.objects.get(user = u.id)
	path = request.FILES['file']	
	handle_uploaded_file(path, user)
	
	success_msg = "Data Uploaded Successfully!!"
	u=get_object_or_404(User, username=user)
	
	t = UserProfile.objects.get(user=u.id)
	date = datetime.date.today()
	start_week = date - datetime.timedelta(date.weekday())
	end_week = start_week + datetime.timedelta(7)
		
	l_list = LogTable.objects.filter(username=u.username, timestamp__range=[start_week, end_week]).order_by('timestamp')
	
	return render_to_response('message/log.html', {'log_list': l_list, 'success_msg': success_msg,
	'user': u,
	'type': t})

def handle_uploaded_file(f, user):
	i = 0
	for line in f:
		print line
		print "'''''"
		log = LogTable()
		if i == 0:
			med_id = line[:-1]
			if med_id == '111':
				med_id = 'Controller1'
			elif med_id == '222':
				med_id = 'Controller2'
			elif med_id == '333':
				med_id = 'Reliever'
			elif med_id == '444':
				med_id = 'Symptom1'
			elif med_id == '555':
				med_id = 'Symptom2'
			elif med_id == '666':
				med_id = 'Symptom3'
			i+=1
		elif i == 1:
			year = line[:-1]
			if len(year) == 2:
				year = '20'+year
			i+=1
		elif i == 2:
			month = line[:-1]
			if len(month) == 1:
				month = '0'+month
			i+=1
		elif i == 3:
			day = line[:-1]
			if len(day) == 1:
				day = '0'+day
			i+=1
		elif i == 4:
			hour = line[:-1]
			if len(hour) == 1:
				hour = '0'+hour
			i+=1
		elif i == 5:
			mins = line[:-1]
			if len(mins) == 1:
				mins = '0'+mins
			
			secs = randint(0,50)
			secs = str(secs)
			if len(secs) == 1:
				secs = '0'+secs
			timestamp = year+'-'+month+'-'+day+" "+hour+':'+mins+":"+secs
			print timestamp
			print "****"
			entry = 'username:'+user+" "+'med_id:'+med_id+" "+'timestamp:'+timestamp
			log.username = user
			log.med_id = med_id
			log.timestamp = timestamp
			log.save()
			i = 0
	
	
	
			
@csrf_exempt
def signup(request):
	form = NewUser(request.POST)
	if form.is_valid():
		pat_username = form.cleaned_data['pat_username']
		pat_first_name = form.cleaned_data['pat_first_name']
		pat_last_name = form.cleaned_data['pat_last_name']
		pat_password = form.cleaned_data['pat_password']
		confirm_password = form.clean_confirm_password()
		if confirm_password is 'set':
			reg_usuc = "Passwords don't match!"
			return render_to_response("message/login.html", {'reg_usuc': reg_usuc})
		pat_email = form.cleaned_data['pat_email']
		pat_type = 1
		par_type = 2
		pat = User.objects.create_user(pat_username, pat_email, pat_password)
		pat.first_name=pat_first_name
		pat.last_name=pat_last_name
		pat.save()

		pat_user = User.objects.get(username=pat_username)
		UserProfile.objects.get_or_create(user=pat, type=pat_type)[0]
		reg_suc = "Registered Successfully!!"
		return render_to_response("message/login.html", {'reg_suc': reg_suc})
	else:
		reg_usuc = "Please enter valid details"
		return render_to_response("message/login.html", {'reg_usuc': reg_usuc})

def login1(request):
	return render_to_response('message/login.html')
	
@csrf_exempt
def login_process(request):
	form = login_form(request.POST)
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:	
				login(request, user)
				t = UserProfile.objects.get(user=user.id)
				if t.type == 1:
					return render_to_response('message/pat.html', {'user': user, "type": t
					}, context_instance=RequestContext(request))
				elif t.type == 2:
					rel_obj = relation_table.objects.get(parent_id = username)
					patient = User.objects.get(username = rel_obj.patient_id)
					return render_to_response('message/pat.html', {'user': user, 
					"type": t,
					"patient": patient
					}, context_instance=RequestContext(request))
		else:
			error_message="incorrect username or password!!"
			return render_to_response('message/login.html', {'error_message': error_message})
		
	else:
		error_message = "Enter the required details"
		return render_to_response('message/login.html', {'error_message': error_message})
		
@csrf_exempt				
def logout1(request):
	logout(request)
	return render_to_response('message/login.html')
				
def pat(request, user):
	u = User.objects.get(username=user)
	t = UserProfile.objects.get(user=u.id)
	return render_to_response('message/pat.html', {'user': u, "type": t
				}, context_instance=RequestContext(request))
	
def par(request, user):
	u = User.objects.get(username=user)
	rel_obj = relation_table.objects.get(parent_id = user)
	patient = User.objects.get(username = rel_obj.patient_id)
	t = UserProfile.objects.get(user=u.id)
	return render_to_response('message/pat.html', {'user': u, 
	"type": t,
	"patient": patient
	}, context_instance=RequestContext(request))

@csrf_exempt
def note(request, user):

	u=get_object_or_404(User, username=user)
	t = UserProfile.objects.get(user=u.id)
	if t.type == 1:
		date = datetime.date.today()
		start_week = date - datetime.timedelta(date.weekday())
		end_week = start_week + datetime.timedelta(6)
		l_note = notes_table.objects.filter(uid=u.id, start_week__range=[start_week, end_week]).order_by('start_week')
		return render_to_response("message/note.html", {'user': u, 'note_list': l_note, 'type': t,'start_week': start_week, 
		'end_week': end_week
		}, context_instance=RequestContext(request))
	else:
		rel_obj = relation_table.objects.get(parent_id = user)
		patient = User.objects.get(username = rel_obj.patient_id)
		date = datetime.date.today()
		start_week = date - datetime.timedelta(date.weekday())
		end_week = start_week + datetime.timedelta(6)
		l_note = notes_table.objects.filter(uid=patient.id, start_week__range=[start_week, end_week]).order_by('start_week')
		return render_to_response("message/note.html", {'user': u, 'note_list': l_note, 
		'start_week': start_week, 
		'end_week': end_week
		}, context_instance=RequestContext(request))		


@csrf_exempt
def note_process(request, user):

	u=get_object_or_404(User, username=user)
	flag = request.POST['flag']
	t = UserProfile.objects.get(user=u.id)
	if t.type == 1:
		if flag == 'set':
			date = datetime.datetime.strptime(request.POST['from_date'], '%Y-%m-%d').date()
			
			start_week = date - datetime.timedelta(date.weekday())
			end_week = start_week + datetime.timedelta(6)

			l_note = notes_table.objects.filter(uid=u.id, start_week__range=[start_week, end_week]).order_by('start_week')
			return render_to_response("message/note.html", {'user': u, 'note_list': l_note, 'type': t,
			'start_week': start_week, 
			'end_week': end_week
			}, context_instance=RequestContext(request))
		
		else:
			date = datetime.datetime.strptime(request.POST['from_date'], '%Y-%m-%d').date()
			note = request.POST['u_note']

			start_week = date - datetime.timedelta(date.weekday())
			end_week = start_week + datetime.timedelta(6)

			u.notes_table_set.create(uid=u.id, start_week = start_week, end_week = end_week, note = note)

			l_note = notes_table.objects.filter(uid=u.id, start_week__range=[start_week, end_week]).order_by('start_week')
			return render_to_response("message/note.html", {'user': u, 'note_list': l_note, 'type': t, 
			'start_week': start_week, 
			'end_week': end_week
			}, context_instance=RequestContext(request))

	else:
		if flag == 'set':
			rel_obj = relation_table.objects.get(parent_id = user)
			patient = User.objects.get(username = rel_obj.patient_id)
			date = datetime.datetime.strptime(request.POST['from_date'], '%Y-%m-%d').date()
			start_week = date - datetime.timedelta(date.weekday())
			end_week = start_week + datetime.timedelta(6)
			l_note = notes_table.objects.filter(uid=patient.id, start_week__range=[start_week, end_week]).order_by('start_week')
			return render_to_response("message/note.html", {'user': u, 'note_list': l_note, 'type': t,
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
	

	t = UserProfile.objects.get(user=u.id)
	date = datetime.date.today()
	start_week = date - datetime.timedelta(date.weekday())
	end_week = start_week + datetime.timedelta(7)
		
	if t.type == 1:

		
		l_list = LogTable.objects.filter(username=u.username, timestamp__range=[start_week, end_week]).order_by('timestamp')
		
		return render_to_response('message/log.html', {'log_list': l_list, 
		'user': u,
		'type': t})
	else:

		rel_obj = relation_table.objects.get(parent_id = user)
		patient = User.objects.get(username = rel_obj.patient_id)
		l_list = LogTable.objects.filter(username=patient.username, timestamp__range=[start_week, end_week]).order_by('timestamp')
		return render_to_response('message/log.html', {'log_list': l_list, 
		'user': u,
		'patient': patient,
		'type': t})


@csrf_exempt	
def date_log(request, user):
	error_message = ""
	#if request.method == "POST":
	u=get_object_or_404(User, username=user)
	t = UserProfile.objects.get(user=u.id)
	form = log_form(request.POST)
	
	if form.is_valid():
		print "asjo"
		start_week = form.cleaned_data['from_date']
		end_week = form.cleaned_data['to_date']
		end_week = end_week + datetime.timedelta(1)
		
		l_list = LogTable.objects.filter(username=u.username, timestamp__range=[start_week, end_week]).order_by('timestamp')
		return render_to_response('message/log.html', {'log_list': l_list, 
		'user': u,
		'type': t})
			
	else:
		error_message = "Please select a range"
		return render_to_response('message/log.html', {'user':u, 'type': t, 'form': form, 'error_message':error_message})

@csrf_exempt
def chartfirst(request, user):
	return render_to_response("message/chart.html")
	
@csrf_exempt	
def char(request, user):
	
	u = get_object_or_404 (User,username = user)
	t = UserProfile.objects.get(user=u.id)
	form = char_form(request.POST)
	if form.is_valid():
		user_date = form.cleaned_data['f_date']
		start_week = user_date - datetime.timedelta(user_date.weekday())
			
		count_reliever = [0 for i in range(8)]
		count_medicine = [0 for i in range(8)]
		count_symptom = [0 for i in range(8)]
		for x in range(1,8):
			end_week = start_week + datetime.timedelta(x)
				
				
			data4 = LogTable.objects.filter(username=u.username, timestamp__range=[start_week, end_week], med_id = 'Controller1').count()
			data5 = LogTable.objects.filter(username=u.username, timestamp__range=[start_week, end_week], med_id = 'Controller2').count()
			data6 = LogTable.objects.filter(username=u.username, timestamp__range=[start_week, end_week], med_id = 'Reliever').count()
				
			count_medicine[x] = data4 + data5 
			count_reliever[x] = data6
				
			sym1 = LogTable.objects.filter(username=u.username, timestamp__range=[start_week, end_week], med_id = 'Symptom1').count()
			sym2 = LogTable.objects.filter(username=u.username, timestamp__range=[start_week, end_week], med_id = 'Symptom2').count()
			sym3 = LogTable.objects.filter(username=u.username, timestamp__range=[start_week, end_week], med_id = 'Symptom3').count()
			count_symptom[x] = sym1 + sym2 + sym3

		m1 = count_medicine[1]
		m2 = count_medicine[2]
		m3 = count_medicine[3]
		m4 = count_medicine[4]
		m5 = count_medicine[5]
		m6 = count_medicine[6]
		m7 = count_medicine[7]
		
		r1 = count_reliever[1]
		r2 = count_reliever[2]
		r3 = count_reliever[3]
		r4 = count_reliever[4]
		r5 = count_reliever[5]
		r6 = count_reliever[6]
		r7 = count_reliever[7]
		s1 = count_symptom[1]
		s2 = count_symptom[2]
		s3 = count_symptom[3]
		s4 = count_symptom[4]
		s5 = count_symptom[5]
		s6 = count_symptom[6]
		s7 = count_symptom[7]
				
		print count_medicine
		print start_week
		print end_week
		return render_to_response('message/chart.html', {'user': u, 'type':t, 'r1':r1, 'r2':r2,'r3':r3,'r4':r4,'r5':r5,'r6':r6,'r7':r7, 'm1' : m1,'m2' : m2,'m3' : m3,'m4' : m4,'m5' : m5,'m6' : m6,'m7' : m7,'s1': s1,'s2': s2,'s3': s3,'s4': s4,'s5': s5,'s6': s6,'s7': s7})
	
	else:
		return render_to_response('message/chart.html', {'user': u,
		'type':t,
		'cherr_message': "Please select a week"
		})
			
def gen_report(request, user):
	u = User.objects.get(username=user)
	t = UserProfile.objects.get(user=u.id)
	return render_to_response ('message/report_page.html', {'user': u, 'type':t})

@login_required
@csrf_exempt
def send_email1(request, user):

	u = User.objects.get(username = user)
	start_week = request.POST['from_date']
	#end_week = request.POST['to_date']
	to_mail = request.POST['to_email']
	t = UserProfile.objects.get(user=u.id)
	from_email = u.email
	user_date = datetime.datetime.strptime(start_week, '%Y-%m-%d').date()
	c_start_week = user_date - datetime.timedelta(user_date.weekday())
	l_start_week = user_date - datetime.timedelta(user_date.weekday())
	l_end_week = l_start_week + datetime.timedelta(7)
	count_reliever = [0 for i in range(8)]
	count_medicine = [0 for i in range(8)]
	count_symptom = [0 for i in range(8)]
	for x in range(1,8):
		c_end_week = c_start_week + datetime.timedelta(x)

		data4 = LogTable.objects.filter(username=u.username, timestamp__range=[c_start_week, c_end_week], med_id = 'Controller1').count()
		data5 = LogTable.objects.filter(username=u.username, timestamp__range=[c_start_week, c_end_week], med_id = 'Controller2').count()
		data6 = LogTable.objects.filter(username=u.username, timestamp__range=[c_start_week, c_end_week], med_id = 'Reliever').count()
		
		
		count_medicine[x] = data4 + data5 
		count_reliever[x] = data6
		
		sym1 = LogTable.objects.filter(username=u.username, timestamp__range=[c_start_week, c_end_week], med_id = 'Symptom1').count()
		sym2 = LogTable.objects.filter(username=u.username, timestamp__range=[c_start_week, c_end_week], med_id = 'Symptom2').count()
		sym3 = LogTable.objects.filter(username=u.username, timestamp__range=[c_start_week, c_end_week], med_id = 'Symptom3').count()
		count_symptom[x] = sym1 + sym2 + sym3

	m1 = count_medicine[1]
	m2 = count_medicine[2]
	m3 = count_medicine[3]
	m4 = count_medicine[4]
	m5 = count_medicine[5]
	m6 = count_medicine[6]
	m7 = count_medicine[7]
		
	r1 = count_reliever[1]
	r2 = count_reliever[2]
	r3 = count_reliever[3]
	r4 = count_reliever[4]
	r5 = count_reliever[5]
	r6 = count_reliever[6]
	r7 = count_reliever[7]
	
	s1 = count_symptom[1]
	s2 = count_symptom[2]
	s3 = count_symptom[3]
	s4 = count_symptom[4]
	s5 = count_symptom[5]
	s6 = count_symptom[6]
	s7 = count_symptom[7]

	l_list = LogTable.objects.filter(username=u.username, timestamp__range=[l_start_week, l_end_week]).order_by('timestamp')

	start_week = user_date - datetime.timedelta(user_date.weekday())
	end_week = start_week + datetime.timedelta(6)
	l_note = notes_table.objects.filter(uid=u.id, start_week__range=[l_start_week, l_end_week]).order_by('start_week')
	
	d=Context({'log_list': l_list, 'note_list': l_note, 'start_week': start_week, 'end_week': end_week, 'user': u, 'type': t, 'r1':r1, 'r2':r2,'r3':r3,'r4':r4,'r5':r5,'r6':r6,'r7':r7, 'm1' : m1,'m2' : m2,'m3' : m3,'m4' : m4,'m5' : m5,'m6' : m6,'m7' : m7,'s1': s1,'s2': s2,'s3': s3,'s4': s4,'s5': s5,'s6': s6,'s7': s7})
	htmly = get_template('message/report.html')
	subject, from_email, to = 'test1', from_email, to_mail
	text_content = 'This is an important message.'
	#html_content = '<p>This is an <strong>important</strong> message.</p>'
	html_content = htmly.render(d)
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()
	return render_to_response("message/report_disp.html", {'log_list': l_list, 'note_list': l_note, 'start_week': start_week, 'end_week': end_week, 'user': u, 'type': t,'r1':r1, 'r2':r2,'r3':r3,'r4':r4,'r5':r5,'r6':r6,'r7':r7, 'm1' : m1,'m2' : m2,'m3' : m3,'m4' : m4,'m5' : m5,'m6' : m6,'m7' : m7,'s1': s1,'s2': s2,'s3': s3,'s4': s4,'s5': s5,'s6': s6,'s7': s7})


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
