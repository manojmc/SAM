from message.models import user_table
from django.contrib import admin

class userAdmin(admin.ModelAdmin):
	search_fields = ['username']

admin.site.register(user_table, userAdmin)
