from django.conf.urls import url
from main import views


urlpatterns = [
    url(r'^wakeup/', views.wakeup, name='wakeup'),
    url(r'^$', views.main, name='main'),
]


