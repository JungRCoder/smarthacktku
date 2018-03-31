from django.conf.urls import url
from userLogin import views


urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    #url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<methods>\w+)/$', views.profile, name='profile'),
    url(r'^password/$', views.password, name='password'),
    url(r'^forgetpassword/$', views.forgetpassword, name='forgetpassword'),
    url(r'^checkVerify/$', views.checkVerify, name='checkVerify'),
    url(r'^init/$', views.init, name='init'),
]