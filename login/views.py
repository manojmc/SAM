from message.models import user_table, message_table, log_table
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login

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
			return HttpResponse("this is the patient page")
			
	
		else:
			return render_to_response('message/add.html')
		
	else:
		return HttpResponse("authentication failed")
		
	
def add_process(request):	
	type=request.POST['type']
	render_to_response('message.check.html')
	
    # Create your views here.
