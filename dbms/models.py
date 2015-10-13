from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    subject = models.CharField(max_length=20)

    def __unicode__(self):
        return self.subject



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    email = models.CharField(max_length = 30)
    username = models.CharField(max_length = 15, unique=True)
    password = models.CharField(max_length = 40)
    proffesion = models.CharField(max_length = 20, null=True)
    cur_university = models.CharField(max_length = 30, null=True)
    sex = models.CharField(max_length=2, null=True)   
    country = models.CharField(max_length = 30, null=True)
    location = models.CharField(max_length = 30,null=True)
    rand = models.CharField(max_length=21, default='NONE',null=True)
    interest_topic = models.ManyToManyField(Topic, default = 'NONE')
    #institute = models.ManyToManyField(Institute, default='NONE')
    def __unicode__(self):
        return self.username
    
class Institute(models.Model):
    user = models.ForeignKey(UserProfile)
    school_name = models.CharField(max_length=30,null=True)
    start_time = models.CharField(max_length=30,null=True)
    end_time = models.CharField(max_length=30,null=True)
    degree = models.CharField(max_length=30,null=True)   

    def __unicode__(self):
        return self.school_name




