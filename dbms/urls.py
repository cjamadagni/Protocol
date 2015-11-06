from django.conf.urls import patterns, include, url
#from dbms.views import lnch,signup,signin,check,edit_profile,add_topic,view_all_papers,addschool,welcome,filterpaper,delete_topic,delete_school,user_logout,sign_up,upload_paper
from dbms.views import *
from papers.views import upload,viewer,add_comment,search
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dbms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^signingin/',lnch),
    url(r'^$',startup),
    url(r'^signup/$',signup),
    url(r'^signin/$',signin),
    url(r'^check/$',check),
    url(r'^editprofile/$',edit_profile),
    url(r'^logout/$',user_logout),
    url(r'^add_topic', add_topic),
    url(r'^dajaxice/', include('dajaxice.urls')),
    url(r'^upload/',upload),
    url(r'^viewer/',viewer),
    url(r'^add_comment/',add_comment),
    url(r'^viewall',view_all_papers),
    #url(r'^search',search),
    url(r'^addschool',addschool),
    url(r'^welcome',welcome),
    url(r'^filter',filterpaper),
    url(r'^delete_topic',delete_topic),
    url(r'^delete_school',delete_school),
    url(r'^signingup',sign_up),
    url(r'^uploadpaper',upload_paper),
    url(r'^mypapers',get_paper_list),
    url(r'^userprofile',get_user_details),
    url(r'^updateinfo',update_user_info),
    url(r'^returnhome',return_home),
    url(r'^email_validate',emailValidate),
    url(r'^searchedpapers',get_searched_papers),
    url(r'^userdetails/(?P<uid>\w+)', userdetails),

    #url(r'^%s/' % '', include('dajaxice.urls')),
    #url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
