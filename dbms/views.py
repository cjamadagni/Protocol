from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.forms import ModelForm
from models import UserProfile,Topic,Institute
from papers.models import Paper
import datetime, sys
import string,random
import json
from one import printit
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import random
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, Http404

from django.conf import settings

def id_generator(size=20, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def int_generate(size=7, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class SignupForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user', 'first_name', 'last_name', 'email', 'username', 'password', 'proffesion', 'cur_university', 'sex', 'country', 'location') 


def lnch(request):
    printit()
    cookie_value = id_generator()
    response = render(request, 'main.html')    
    response.set_cookie('id', cookie_value)
    return response

#Added by me
def startup(request):
    response = render(request, 'homepage.html')
    return response
    

#Added by me
def sign_up(request):
    printit()
    cookie_value = id_generator()
    response = render(request, 'Signup.html')
    response.set_cookie('id', cookie_value)
    return response

#Added by me to transfer control to the upload paper html page
def upload_paper(request):
    printit()
    cookie_value = id_generator()
    response = render(request, 'upload.html')
    response.set_cookie('id', cookie_value)
    return response

def user_logout(request):
    logout(request)
    return render(request, 'homepage.html')

def return_home(request):
    return render(request,'profilehome.html')

#Getting the user profile of the comment author
def userdetails(request,uid):
    userprofile = UserProfile.objects.get(username=uid)
    user_details = {'first_name':userprofile.first_name, 'last_name':userprofile.last_name, 'email':userprofile.email, 'cur_university':userprofile.cur_university, 'profession':userprofile.proffesion}
    return render(request, 'usrdetails.html',{'userdetails': user_details})


    


def signup(request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        try:
            pwd = request.POST['pass']
        except:
            pwd = ''    
        profession = request.POST['profession']
        cur_university = request.POST['cur_university']
        #sex = request.POST['sex']
        #country = request.POST['country']
        #location = request.POST['location']
        #data = {'first_name': fname, 'last_name': lname, 'email': email, 'username': username, 'password': pwd, 'proffesion': proffesion, 'cur_university': cur_university, 'sex': sex, 'country': country, 'location': location}
       
        try:
            user = User.objects.create_user(username,email,pwd)
            user.save()
        except:
            error = {'error': 'username already taken'}
            return render(request, 'error.html', error)
        #data = {'user':user,'first_name': fname, 'last_name': lname, 'email': email, 'username': username, 'password': pwd, 'proffesion': 'NULL', 'cur_university': cur_university, 'sex': 'M', 'country': 'NULL', 'location': 'NULL'} 
        #form = SignupForm(data)
        userprofile = UserProfile.objects.create(user=user,first_name=fname,last_name=lname,email=email,username=username,password=pwd,proffesion=profession,cur_university=cur_university,sex='M',country= 'NULL',location='NULL')
        userprofile.save()
        n=random.randint(1000,9999)
        request.session['randkey'] = str(n)
        email = EmailMessage('Protocol Team', 'Your account creation key is '+str(n)+'. Enter this to procced\nThank you', to=[email])
        email.send()
    
    return render(request, 'emailvalidation.html') 



def emailValidate(request):
    if request.method == 'POST':
        key = request.POST['key']

        if key == request.session['randkey']:
            return HttpResponseRedirect('/signingin/')
        else:
            error = {'error': 'Invalid Key'}
            return render(request, 'error.html', error)


            

            
def get_session_cookie(request):
    if request.COOKIES.has_key('id'):
        value = request.COOKIES('id')
        return value
    

"""def get_paper_list(cookie_data):
    result = UserProfile.objects.get(rand=cookie_data)
    paper_data = Paper.objects.filter(UserProfile=result)
    paper_list = []
    if paper_data:
        for data in paper_data:
            #paper_list.append(data.title)
            paper_list.append({'title': data.title, 'link': data.id})
    return paper_list """

def get_paper_list(request):
    userprofile = UserProfile.objects.get(user = request.user)
    paper_data = Paper.objects.filter(UserProfile = userprofile)
    paper_list = []
    if paper_data:
        for data in paper_data:
            paper_list.append({'title': data.title, 'link': data.id, 'description':data.description})

    return render(request, 'allpapers.html',{'paper_list': paper_list})

def get_user_details(request):
    userprofile = UserProfile.objects.get(user=request.user)
    user_details = {'first_name':userprofile.first_name, 'last_name':userprofile.last_name, 'email':userprofile.email, 'cur_university':userprofile.cur_university, 'profession':userprofile.proffesion}
    return render(request, 'userprofile.html',{'userdetails': user_details})    

#Search filter
def get_searched_papers(request):
    if request.method=='POST':
        broadDomain = request.POST['broadDomain']
        papername = request.POST['papername']
        userprofile = UserProfile.objects.get(user=request.user)
        paper_list = []
        if papername == "None":
            paper_data = Paper.objects.filter(Q(broadDomain1=broadDomain) | Q(broadDomain2=broadDomain)).order_by('-rating').order_by('-views')
        else:
            paper_data = Paper.objects.filter(Q(broadDomain1=broadDomain) | Q(broadDomain2=broadDomain)).filter(title__contains=papername).order_by('-rating').order_by('-views')

        if paper_data:
            for data in paper_data:
                paper_list.append({'title': data.title, 'link': data.id, 'description':data.description})

            return render(request, 'searchedpapers.html',{'paper_list': paper_list})
        
        else:
            return render(request, 'error.html',{'error': 'No papers which match the search parameters'})

        

        

#updating the new profile info in the DB
def update_user_info(request):
    if request.method=='POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        cur_university = request.POST['cur_university']
        profession = request.POST['profession']
        userprofile = UserProfile.objects.get(user=request.user)
        userprofile.first_name = fname
        userprofile.last_name = lname
        userprofile.email = email
        userprofile.cur_university = cur_university
        userprofile.proffesion = profession
        userprofile.save()
        return render(request, 'profilehome.html')





def pfilter():
    pass




def filterpaper(request):
    p=[]
    paper_list=[]
    if request.method=='POST':
        sub = request.POST['subject']
        pap = Paper.objects.filter(tags=sub)
        t = get_all_topic()
        for i in pap:
            print p.append(i.id)
            paper = Paper.objects.get(id=i.id)
            paper_list.append({'title': paper.title, 'link': paper.id})
    return render(request, 'all.html', {'paper_list': paper_list,'topics':t})

    




def get_paper_list_from_UserProfile(result):
    #result = UserProfile.objects.get(rand=cookie_data)
    paper_data = Paper.objects.filter(UserProfile=result)
    paper_list = []
    if paper_data:
        for data in paper_data:
            #paper_list.append(data.title)
            paper_list.append({'title': data.title, 'link': data.id})
    return paper_list


def get_all_papers(request):
    print settings.MEDIA_ROOT
    result = Paper.objects.all()
    paper_list = []
    if result:
        for paper in result:
            UserProfile = UserProfile.objects.get(id=paper.UserProfile_id)
            paper_list.append({'title': paper.title, 'link': paper.id, 'UserProfile': UserProfile.username})
        print paper_list
    return paper_list
    

               
"""def signin(request):
    results = {}
    print "everytime i come here print it"
    if request.method == 'POST':
        uname = request.POST['username'];
        pwd = request.POST['pass'];
        print uname
        print UserProfile.objects.all()
        if not UserProfile.objects.filter(username = uname).count()==0:
            try:
                results=UserProfile.objects.get(username=uname)
            except:
                print sys.exc_info()    
                   
            if pwd==results.password:
                cookie_data = request.COOKIES.get('id')
                print cookie_data
                results.rand = cookie_data
                results.save()
                paper_list = get_paper_list(cookie_data)
                #return render(request,'profile.html',{'firstname': results.first_name, 'lastname': results.last_name, 'paper_list': paper_list});
                #return render(request,'upload.html',{'firstname': results.first_name, 'lastname': results.last_name, 'paper_list': paper_list});
                return render(request,'profilehome.html',{'firstname': results.first_name, 'lastname': results.last_name, 'paper_list': paper_list});
                #return render(request,'allpapers.html',{'firstname': results.first_name, 'lastname': results.last_name, 'paper_list': paper_list});
            else: 
                error =  {'error': 'password or username do not match'}     
        else:
            error = {'error': 'username do not exist'}
    return render(request, 'error.html', error) """ 

def signin(request):
    username = request.POST['username']
    password = request.POST['pass']
    results = {}
    User= authenticate(username=username, password=password)
    if User is not None:
        if User.is_active:
            login(request, User)
            try:
                results=User.objects.get(username=uname)
            except:
                print sys.exc_info()
            
            return render(request,'profilehome.html')

            
        else:
            # Return a 'disabled account' error message
            error =  {'error': 'Invalid log in credentials'}
    else:
        error = {'error': 'Invalid log in credentials'}
    return render(request, 'error.html', error)



def check(request):
    if request.is_ajax():
        if request.method=='POST':
            uname = request.POST['username']
            print uname
            if UserProfile.objects.filter(username=uname).exists():
                print 'Raw Data: "%s"' % request.body
                msg = 1
            else:
                msg = 0
    return HttpResponse(json.dumps({'data': msg}))

def print_topic(request, cookie_data):
    topics = []
    result_set = UserProfile.objects.get(rand = cookie_data)
    result = UserProfile.objects.filter(rand = cookie_data)
    try:
        result_topic = result.values('interest_topic')
        print result_topic
        for item in result_topic:
            topics.append(Topic.objects.get(id=item['interest_topic']).subject)
    except: 
        topics.append("There are no topics")
    return (result_set, topics)

def get_all_topic():
    topics = [] 
    result = Topic.objects.all()
    for item in result:
        topics.append({'value': item.id, 'title': item.subject})
    return topics


def get_schooling(request):
    cookie_data = request.COOKIES.get('id')
    if UserProfile.objects.filter(rand = cookie_data).exists():
        result = UserProfile.objects.get(rand=cookie_data)
        result_set=Institute.objects.filter(UserProfile=result.id)
    return result_set
                



def edit_profile(request):
    userprofile = UserProfile.objects.get(user=request.user)
    user_details = {'first_name':userprofile.first_name, 'last_name':userprofile.last_name, 'email':userprofile.email, 'cur_university':userprofile.cur_university, 'profession':userprofile.proffesion}
    return render(request, 'editprofile.html',{'userdetails': user_details})

    


def delete_topic(request):
    if request.method == 'POST':
        sub = request.POST['subject']
        t=Topic.objects.get(id=sub)
        #t.objects.get(interest_topic=t)
        u=get_UserProfile(request)
        u.interest_topic.remove(t)
    return render(request,'thanks.html',{'message': "Topic Deleted"})

def delete_school(request): 
    if request.method=='POST':
        s = request.POST['sch']
        t = Institute.objects.filter(id=s).delete()
    return render(request,'thanks.html',{'message': "School Deleted"})


def check_cookie_validity(request):
    try:
        cookie_data = request.COOKIES.get('id')
    except:
        return False
    if UserProfile.objects.filter(rand = cookie_data).exists():
        return True
    else:
        return False
        
def get_UserProfile(request):  
    cookie_data = request.COOKIES.get('id')
    if UserProfile.objects.filter(rand = cookie_data).exists():
        result = UserProfile.objects.get(rand=cookie_data)
    return result

def add_topic(request):
    if check_cookie_validity(request):
        if request.method == 'POST':
            topic = request.POST['subject']
            print topic
            cookie_data = request.COOKIES.get('id')
            result = UserProfile.objects.get(rand=cookie_data)
            result.interest_topic.add(int(topic))
            return render(request, 'thanks.html', {'message': 'Topic has been added'})   
            #result = UserProfile.objects.get(rand=cookie_data)
            #(result1, result2) = print_topic(request,cookie_data)
            #result3 = get_all_topic()
            #return render(request, 'edit_profile.html',{'firstname': result1.first_name, 'lastname': result1.last_name, 'interest_topic': result2,'topics': result3})
            #result_topic = result.values('interest_topic')[0]
            #return render(request, 'edit_profile.html')
    else:
        return render(request, '404.html')


def view_all_papers(request):
    paper_list = get_all_papers(request)
    t = get_all_topic()
    if check_cookie_validity(request):
        return render(request, 'all.html', {'paper_list': paper_list,'topics':t})
    else:
        return render(request, 'ws_all.html',{'paper_list': paper_list})

def addschool(request):
    if request.method=='POST':  
        skl=request.POST['school_name']
        sd=request.POST['st_date']
        ed=request.POST['end_date']
        deg=request.POST['degree_at']
        u=get_UserProfile(request) 
        data=Institute(UserProfile=u,school_name=skl,start_time=sd,end_time=ed,degree=deg)
        data.save()
        return render(request,'thanks.html',{'message':'Schooling details has been saved'})

def welcome(request):
    cookie_data=request.COOKIES.get('id')    
    u = get_UserProfile(request)
    papers = get_paper_list_from_UserProfile(u)
    top = print_topic(request,cookie_data)
    top = top[1]
    return render(request,'welcome.html', {'UserProfile': u, 'interest_topic': top,'paper_list':papers})
