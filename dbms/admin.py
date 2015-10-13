from django.contrib import admin
from dbms.models import UserProfile,Topic
from papers.models import Paper

admin.site.register(UserProfile)
admin.site.register(Topic)
admin.site.register(Paper)
