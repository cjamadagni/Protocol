from django.shortcuts import render
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.forms import ModelForm
from django import forms
from dbms.models import UserProfile,Topic
from models import Paper,Comment,View
import datetime, sys
import string,random
import json,sys
from subprocess import call
from django.conf import settings
import os
class UploadForm(ModelForm):
    class Meta:
        model=Paper
        fields=('title','paper_file','broadDomain1','broadDomain2')


class UploaderForm(forms.Form):
    upload = forms.FileField()


    def clean_upload():
        upload = self.cleaned_data['upload']
        content_type = upload.content_type
        if content_type in settings.CONTENT_TYPES:
            if upload._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s')\
                       % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(upload._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))

        return upload


def get_UserProfile_fromcookie(request):
    cookie_data = request.COOKIES.get('id')
    if UserProfile.objects.filter(rand = cookie_data).exists():
        result_set = UserProfile.objects.get(rand = cookie_data)
        return result_set



def get_paper_fromid(paper_id):
    try:
        result = Paper.objects.get(id=paper_id)
    except:
        print sys.exc_info
    return result

def convert(filename):
    l = os.path.join(os.path.dirname(__file__), '..', 'media/uploads/')
    l = l+filename
    call(['pdftotext',l])


"""def upload(request):
    if request.method =='POST':
        t = []
        #form = UploaderForm(request.POST,request.FILES)
        #if form.is_valid():
        paper_title=request.FILES['ups'].name
        uploaded=request.FILES['ups']
        tags = request.POST['tags']
        #HARD CODING THE TAG
        #tags = 'Networks,Algorithms'
        t = tags.split(',')
        print t
        p = []
        
        for i in range(len(t)-1):
            l = Topic.objects.get(subject=t[i].encode('ascii','replace'))
            p.append(l.id)
        #print uploaded
        print p
        #print uploaded.size
        username = get_UserProfile_fromcookie(request)        
        data = {'title': paper_title,'paper_file':uploaded}
        form = UploadForm(data)
        if not Paper.objects.filter(title=paper_title).count()==0:
            error={'error':'file already present'}
            return render(request, 'error.html', error)
        obj = Paper(title=paper_title,paper_file=uploaded,UserProfile=username)
        obj.save()
        pap = Paper.objects.get(title=paper_title)
        for i in p:
            pap.tags.add(int(i))
        convert(paper_title)
        #form.save()
        '''
        if form.is_valid():
            form.save()
        else:
            print form.errors
        '''
        #return HttpResponse("errros")
        return render(request,'thanks.html',{'message': 'Research Paper Uploaded'}) """

def upload(request):
    if request.method=='POST':
        t = []
        paper_title=request.FILES['ups'].name
        uploaded=request.FILES['ups']
        broadDomain1 = request.POST['broadDomain1']
        broadDomain2 = request.POST['broadDomain2']
        description = request.POST['description']
        conference = request.POST['conference']
        #tags = request.POST['tags']
        #t = tags.split(',')
        #print t
        #p = []
        #for i in range(len(t)-1):
        #    l = Topic.objects.get(subject=t[i].encode('ascii','replace'))
        #    p.append(l.id) 
        #print uploaded
        #print p
        userprofile = UserProfile.objects.get(user = request.user)
        username = request.user.username
        #data = {'title': paper_title,'paper_file':uploaded,'broadDomain1':broadDomain1,'broadDomain2':broadDomain2}
        #form = UploadForm(data)
        if not Paper.objects.filter(title=paper_title).count()==0:
            error={'error':'file already present'}
            return render(request, 'error.html', error)

        if (".pdf" in str(paper_title)) or (".docx" in str(paper_title)):               
            paper = Paper.objects.create(title=paper_title,paper_file=uploaded,UserProfile=userprofile,views=0,broadDomain1=broadDomain1,broadDomain2=broadDomain2, description=description, conference=conference)

            convert(paper_title)
            return render(request,'thanks.html',{'message': 'Research Paper Uploaded'})
        else:
            return render(request,'thanks.html',{'message': 'Unsupported File type'})
        



def get_paper_comments(paper_id):
    try:
        comment_list = Comment.objects.filter(paper_id=paper_id).order_by('-comment_time')

        print comment_list
    except:
        print sys.exc_info()
        comment_list = []
    
    return comment_list 

"""def viewer(request):
    paper_id = request.GET['id']
    result = Paper.objects.get(id=paper_id)
    cookie_data = request.COOKIES.get('id')
    if UserProfile.objects.filter(rand = cookie_data).exists():
        print "here i am"
        u=UserProfile.objects.get(rand=cookie_data)      
        if View.objects.filter(UserProfile=u,pap=result).exists():
            pass
        else:
            d=View(UserProfile=u,pap=result)
            result.views+=1
            d.save()
    else:
        result.views+=1
        print result.views
    result.save()
    print "this is paper_id",paper_id
    url=result.paper_file.url
    title = result.title
    comment_list = get_paper_comments(paper_id)
    paper = {'url': url, 'title': title,'comment_list': comment_list,'paper_id': paper_id,'views': result.views}
    return render(request, 'frame.html',{'paper': paper})
    #return redirect(url)
    #return HttpResponse(paper_id) """

def viewer(request):
    paper_id = request.GET['id']
    result = Paper.objects.get(id=paper_id)
    userprofile = UserProfile.objects.get(user = request.user)
    #incrementing the view count
    result.views+=1
    print result.views
    result.save()
    url=result.paper_file.url
    title = result.title
    comment_list = get_paper_comments(paper_id)
    comment_list.reverse()
    conference = result.conference
    paper = {'url': url, 'title': title,'comment_list': comment_list,'paper_id': paper_id,'views': result.views, 'conference' : conference}
    #return render(request, 'frame.html',{'paper': paper})
    return render(request, 'viewpaper.html',{'paper': paper})



def add_comment(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        content = request.POST['content']
        paper_id = request.POST['paper_id']
        paper = Paper.objects.get(id=paper_id)
        result = paper
        try:
            userprofile = UserProfile.objects.get(user = request.user)
            print userprofile
        except:
            print sys.exc_info()        
        obj = Comment(UserProfile_id=userprofile,subject=subject,content=content,paper_id=paper)
        obj.save()

        url=result.paper_file.url
        title = result.title
        comment_list = get_paper_comments(paper_id)
        paper = {'url': url, 'title': title,'comment_list': comment_list,'paper_id': paper_id,'views': result.views}
        #return render(request, 'frame.html',{'paper': paper})
        return render(request, 'viewpaper.html',{'paper': paper})
        #return HttpResponse(json.dumps({'status': '200'}))

    return HttpResponse(json.dumps({'status': 501}))


def listen(request):
    pass

def search(request):
    p = []
    s = []
    if request.method=='POST':
        key = request.POST['key']
        if Topic.objects.filter(subject=key).exists():
            topic_id=Topic.objects.get(subject=key)
            #print topic_id.id
            pap = Paper.objects.filter(tags=topic_id)
            for i in pap:
                print p.append(i.id)
                paper = Paper.objects.get(id=i.id)
                s.append({'title': paper.title, 'link': paper.id})
        else:
            return render(request,'thanks.html',{'message':'Topic doesnt exists'})
    return render(request, 'found.html', {'keyword':key,  'paper_list': s})

