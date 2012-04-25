from django.db import models
from django.contrib.auth.models import User
from django import forms

class log_form(forms.Form):
    from_date = forms.DateTimeField()
    to_date = forms.DateTimeField()

class char_form(forms.Form):
	f_date = forms.DateTimeField()

class NewUser(forms.Form):
	pat_username = forms.CharField(max_length=50)
	pat_first_name = forms.CharField(max_length=50)
	pat_last_name = forms.CharField(max_length=50)
	pat_email = forms.EmailField(max_length=75)
	pat_password = forms.CharField(min_length=5, max_length=30, widget=forms.PasswordInput(render_value=False))
	pat_confirm_password = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False))

	def clean_confirm_password(self):
		confirm_password = self.cleaned_data['pat_confirm_password']
		original_password = self.cleaned_data.get('pat_password', '')
		
		if original_password != confirm_password:
			flag = "set"
			return flag
		else:
			return confirm_password

class login_form(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50)


class user_table(models.Model):
	username=models.CharField(max_length=10)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	password=models.CharField(max_length=12)
	type=models.IntegerField()
	def __unicode__(self):
		return self.username
		
class message_table(models.Model):
	user = models.ForeignKey(user_table)
	sender = models.CharField(max_length=10)
	reciever = models.CharField(max_length=10)
	message = models.CharField(max_length=200)
	def __unicode__(self):
		return self.message
		
class med_table(models.Model):
	medicine = models.CharField(max_length=50)
	#med_id = models.CharField(max_length=5)
	def __unicode__(self):
		return self.medicine
		
class log_table(models.Model):
	uid = models.ForeignKey(user_table)
	med_id = models.ForeignKey(med_table)
	timestamp = models.DateTimeField()
	def __unicode__(self):
		return self.timestamp

class notes_table(models.Model):
	uid = models.ForeignKey(User)
	start_week = models.DateTimeField()
	end_week = models.DateTimeField()
	note = models.CharField(max_length=160)
	def __unicode__(self):
		return self.note

class relation_table(models.Model):
	parent_id = models.CharField(max_length=10)
	patient_id = models.CharField(max_length=10)
	def __unicode__(self):
		return self.parent_id
		
class LogTable(models.Model):
    username = models.CharField(max_length=20)
    med_id = models.CharField(max_length=64)
    timestamp = models.DateTimeField()
    
    def __unicode__(self):
        return "%s, %s (%s)" % (self.username, self.med_id, self.timestamp) 

    class Meta:
        ordering = ['timestamp']

class log(models.Model):
	username = models.CharField(max_length=50)
	med_id = 	models.CharField(max_length=2)
	timestamp = models.DateTimeField()
	
	def __unicode__(self):
		return "%s %s (%s)" % (self.username, self.med_id, self.timestamp)
	class Meta:
		ordering = ['timestamp']

# Create your models here.
