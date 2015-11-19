from django.contrib import admin
from dbms.models import UserProfile,Topic
from papers.models import Paper

class UserProfileAdmin(admin.ModelAdmin):
	fields = ('user','first_name','last_name','email','username','proffesion','cur_university')


admin.site.register(Topic)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Paper)


