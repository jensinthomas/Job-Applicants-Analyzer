"""resume_parser.parser_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('homepage', views.homepage, name='homepage'),
    path('signuppage', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login_page', views.login_page, name='login_page'),
    re_path(r'^logout$', views.logout, name='logout'),
    path('home', views.home, name='home'),
    path('pyresults', views.pyresults, name='pyresults'),
    path('trresults', views.trresults, name='trresults'),
    path('hrresults', views.hrresults, name='hrresults'),
    path('jvresults', views.jvresults, name='jvresults'),
    path('teresults', views.teresults, name='teresults'),
    path('manresults', views.manresults, name='manresults'),
    path(r'^new/(?P<id>\d+)/$', views.new, name='new'),
    path('login', views.login, name='login'),
    path('mainhome', views.mainhome, name='mainhome'),
    path('', views.mainhome, name='mainhome'),
    path('aboutus', views.aboutus, name='aboutus'),
    path(r'^apply/(?P<id>\d+)/$', views.apply, name='apply'),
    path('availablejobs', views.availablejobs, name='availablejobs'),
    path('apply', views.apply, name='apply'),
    path('gallery', views.gallery, name='gallery'),
    path('thankyou', views.thankyou, name='thankyou'),
    path('addjob', views.addjob, name='addjob'),
    path('adminhome', views.adminhome, name='adminhome'),
    path('viewapplicants', views.viewapplicants, name='viewapplicants'),
    path('newjob', views.newjob, name='newjob'),
    path('adlogin_page', views.adlogin_page, name='adlogin_page'),
    path('adminlogin', views.adminlogin, name='adminlogin'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
