from django.db import models
from dbms.models import UserProfile, Topic
import datetime
'''
class Author(models.Model):
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=40)
    email = models.EmailField()
    
    def Meta(self):
        return self.name
'''        

class Paper(models.Model):
    title = models.CharField(max_length=200,default=None)
    paper_file = models.FileField(upload_to='uploads')
    UserProfile = models.ForeignKey(UserProfile)
    #tags = models.ManyToManyField(Topic, default='NONE',null=True)
    views = models.IntegerField(default=0)
    broadDomain1 = models.CharField(max_length=100,default='null', null=True)
    broadDomain2 = models.CharField(max_length=100,default='null', null=True)
    description = models.TextField(null=True,default='null')
    conference = models.CharField(max_length=200,null=True,default='null')
    #authors = models.ManyToManyField(Author, default=None)
    #UserProfile_id = models.ForeignKey(UserProfile)
    #date_publish = models.CharField(max_length=12,default=None)
    
    def __unicode__(self):
        return self.title
    
    
class Comment(models.Model):
    UserProfile_id = models.ForeignKey(UserProfile)
    subject = models.CharField(max_length=100, default="no subject")
    content = models.CharField(max_length=200, default="no content")
    paper_id = models.ForeignKey(Paper)
    comment_time = models.DateTimeField('date_created', default=datetime.datetime.now())

    def __unicode__(self):
        return self.subject


class View(models.Model):
    UserProfile=models.ForeignKey(UserProfile)
    pap=models.ForeignKey(Paper)   

# Create your models here.
