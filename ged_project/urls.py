"""ged_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin 
from django.urls import path, include, re_path

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import views as auth_views

from ged_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inscrire, name='inscrire'),
    path('login/', views.connecter, name="connecter"),
    path('logout/', views.deconnecter, name="deconnecter"),

    path('page/', views.page, name='page'),
    path('compte/', views.page_eleve, name='page_eleve'),
    path('compte/parametres/', views.user_param, name='parametres'),

    path('compte/doc/', views.liste_doc, name = 'liste_doc'),
    path('compte/publier/', views.upload_doc, name = 'upload_doc'),

    path('compte/classe/tc1/', views.doc_tc1, name='tc1'),
    path('compte/classe/tc2/', views.doc_tc2, name='tc2'),
    path('compte/classe/dic1/', views.doc_dic1, name='dic1'),
    path('compte/classe/dic2/', views.doc_dic2, name='dic2'),
    path('compte/classe/dic3/', views.doc_dic3, name='dic3'),

    path('compte/genie/tc/', views.doc_gtc, name='tc'),
    path('compte/genie/git/', views.doc_git, name='git'),
    path('compte/genie/gc/', views.doc_gc, name='gc'),
    path('compte/genie/gem/', views.doc_gem, name='gem'),


    re_path(r'^compte/doc/comment/(?P<pk>[0-9]*)/$', views.comments, name='comments'),
    #path('compte/doc/comment/<int:pk>/', views.comments, name='comments'),
    path('poser/', views.question, name='questions'),
    re_path(r'^compte/question/reponse/(?P<pk>[0-9]*)/$', views.repondre, name='repondre'), 
    
    
    # urls de récupération du mot de passe
    path('reset_password/', auth_views.PasswordResetView.as_view( template_name="ged_app/recuperation/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view( template_name="ged_app/recuperation/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view( template_name="ged_app/recuperation/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view( template_name="ged_app/recuperation/password_reset_done.html"), name='password_reset_complete'),


    #path('docform/', views.publier, name='docform'),
    #path('', include('ged_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)